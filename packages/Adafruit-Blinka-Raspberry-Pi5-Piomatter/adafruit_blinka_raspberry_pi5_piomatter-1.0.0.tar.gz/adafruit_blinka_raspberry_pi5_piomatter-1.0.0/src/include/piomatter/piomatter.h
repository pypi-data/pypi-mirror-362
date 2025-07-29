#pragma once

#include <thread>

#include "hardware/pio.h"

#include "piomatter/buffer_manager.h"
#include "piomatter/matrixmap.h"
#include "piomatter/pins.h"
#include "piomatter/protomatter.pio.h"
#include "piomatter/render.h"

namespace piomatter {

static int pio_sm_xfer_data_large(PIO pio, int sm, int direction, size_t size,
                                  uint32_t *databuf) {
#if 0
    // it would be NICE to gracefully fall back to blocked transfer, but sadly
    // once the large xfer ioctl fails, future small xfers fail too.
    static enum { UNKNOWN, OK, BAD } large_xfer_status = UNKNOWN;
    printf("large_xfer_status=%d\n", large_xfer_status);
    if (large_xfer_status != BAD) {
        int r = pio_sm_xfer_data(pio, sm, direction, size, databuf);
        if (large_xfer_status == UNKNOWN && r != 0) {
            large_xfer_status = BAD;
            fprintf(stderr,
                    "Transmission limit workaround engaged. May reduce quality of "
                    "output.\nSee https://github.com/raspberrypi/utils/issues/123 "
                    "for details.\n");
        } else {
            if (large_xfer_status == UNKNOWN && r == 0) {
                large_xfer_status = OK;
            }
            return r;
        }
    }
#endif
    constexpr size_t MAX_XFER = 65532;
    while (size) {
        size_t xfersize = std::min(size_t{MAX_XFER}, size);
        int r = pio_sm_xfer_data(pio, sm, direction, xfersize, databuf);
        if (r != 0) {
            return r;
        }
        size -= xfersize;
        databuf += xfersize / sizeof(*databuf);
    }
    return 0;
}

static uint64_t monotonicns64() {
    struct timespec tp;
    clock_gettime(CLOCK_MONOTONIC, &tp);
    return tp.tv_sec * UINT64_C(1000000000) + tp.tv_nsec;
}

constexpr size_t MAX_XFER = 65532;

struct piomatter_base {
    piomatter_base() {}
    piomatter_base(const piomatter_base &) = delete;
    piomatter_base &operator=(const piomatter_base &) = delete;

    virtual ~piomatter_base() {}
    virtual int show() = 0;

    double fps;
};

template <class pinout = adafruit_matrix_bonnet_pinout,
          class colorspace = colorspace_rgb888>
struct piomatter : piomatter_base {
    using buffer_type = std::vector<uint32_t>;
    using bufseq_type = std::vector<buffer_type>;
    piomatter(std::span<typename colorspace::data_type const> framebuffer,
              const matrix_geometry &geometry)
        : framebuffer(framebuffer), geometry{geometry}, converter{},
          blitter_thread{} {
        if (geometry.n_addr_lines > std::size(pinout::PIN_ADDR)) {
            throw std::runtime_error("too many address lines requested");
        }
        program_init();
        blitter_thread = std::move(std::thread{&piomatter::blit_thread, this});
        show();
    }

    int show() override {
        int err = pending_error_errno.exchange(0); // we're handling this error
        if (err != 0) {
            return err;
        }
        int buffer_idx = manager.get_free_buffer();
        auto &bufseq = buffers[buffer_idx];
        bufseq.resize(geometry.schedules.size());
        auto converted = converter.convert(framebuffer);
        auto old_active_time = geometry.schedules.back().back().active_time;
        for (size_t i = 0; i < geometry.schedules.size(); i++) {
            protomatter_render_rgb10<pinout>(bufseq[i], geometry,
                                             geometry.schedules[i],
                                             old_active_time, converted.data());
            old_active_time = geometry.schedules[i].back().active_time;
        }
        manager.put_filled_buffer(buffer_idx);
        return 0;
    }

    ~piomatter() {
        if (pio != NULL && sm >= 0) {

            pin_deinit_one(pinout::PIN_OE);
            pin_deinit_one(pinout::PIN_CLK);
            pin_deinit_one(pinout::PIN_LAT);

            for (const auto p : pinout::PIN_RGB)
                pin_deinit_one(p);

            for (size_t i = 0; i < geometry.n_addr_lines; i++) {
                pin_deinit_one(pinout::PIN_ADDR[i]);
            }
            pio_sm_unclaim(pio, sm);
        }

        manager.request_exit();
        if (blitter_thread.joinable()) {
            blitter_thread.join();
        }
    }

  private:
    void program_init() {
        pio = pio0;
        sm = pio_claim_unused_sm(pio, true);
        if (sm < 0) {
            throw std::runtime_error("pio_claim_unused_sm");
        }
        int r = pio_sm_config_xfer(pio, sm, PIO_DIR_TO_SM, MAX_XFER, 3);
        if (r) {
            throw std::runtime_error("pio_sm_config_xfer");
        }

        static const struct pio_program protomatter_program = {
            .instructions = protomatter,
            .length = 32,
            .origin = -1,
        };

        uint offset = pio_add_program(pio, &protomatter_program);
        if (offset == PIO_ORIGIN_INVALID) {
            throw std::runtime_error("pio_add_program");
        }

        pio_sm_clear_fifos(pio, sm);
        pio_sm_set_clkdiv(pio, sm, 1.0);

        pio_sm_config c = pio_get_default_sm_config();
        sm_config_set_wrap(&c, offset + protomatter_wrap_target,
                           offset + protomatter_wrap);
        // 1 side-set pin
        sm_config_set_sideset(&c, 2, true, false);
        sm_config_set_out_shift(&c, /* shift_right= */ false,
                                /* auto_pull = */ true, 32);
        sm_config_set_fifo_join(&c, PIO_FIFO_JOIN_TX);
        // Due to https://github.com/raspberrypi/utils/issues/116 it's not
        // possible to keep the RP1 state machine fed at high rates. This target
        // frequency is approximately the best sustainable clock with current
        // FW & kernel.
        constexpr double target_freq =
            2700000 * 2; // 2.7MHz pixel clock, 2 PIO cycles per pixel
        double div = clock_get_hz(clk_sys) / target_freq;
        sm_config_set_clkdiv(&c, div);
        sm_config_set_out_pins(&c, 0, 28);
        sm_config_set_sideset_pins(&c, pinout::PIN_CLK);
        pio_sm_init(pio, sm, offset, &c);
        pio_sm_set_enabled(pio, sm, true);

        pin_init_one(pinout::PIN_OE);
        pin_init_one(pinout::PIN_CLK);
        pin_init_one(pinout::PIN_LAT);

        for (const auto p : pinout::PIN_RGB)
            pin_init_one(p);

        for (size_t i = 0; i < geometry.n_addr_lines; i++) {
            pin_init_one(pinout::PIN_ADDR[i]);
        }
    }

    void pin_init_one(int pin) {
        pio_gpio_init(pio, pin);
        pio_sm_set_consecutive_pindirs(pio, sm, pin, 1, true);
    }

    void pin_deinit_one(int pin) {
        pio_gpio_init(pio, pin);
        pio_sm_set_consecutive_pindirs(pio, sm, pin, 1, false);
    }

    void blit_thread() {
        int cur_buffer_idx = buffer_manager::no_buffer;
        int buffer_idx;
        int seq_idx = -1;
        uint64_t t0, t1;
        t0 = monotonicns64();
        while ((buffer_idx = manager.get_filled_buffer()) !=
               buffer_manager::exit_request) {
            if (buffer_idx != buffer_manager::no_buffer) {
                if (cur_buffer_idx != buffer_manager::no_buffer) {
                    manager.put_free_buffer(cur_buffer_idx);
                }
                cur_buffer_idx = buffer_idx;
            }
            if (cur_buffer_idx != buffer_manager::no_buffer) {
                const auto &cur_buf = buffers[cur_buffer_idx];
                seq_idx = (seq_idx + 1) % cur_buf.size();
                const auto &data = cur_buf[seq_idx];
                auto datasize = sizeof(uint32_t) * data.size();
                auto dataptr = const_cast<uint32_t *>(&data[0]);
                // returns err = rp1_ioctl.... which seems to be a negative
                // errno value
                int r = pio_sm_xfer_data_large(pio, sm, PIO_DIR_TO_SM, datasize,
                                               dataptr);
                if (r != 0) {
                    pending_error_errno.store(errno);
                    printf("xfer_data() returned error %d (errno=%s)\n", r,
                           strerror(errno));
                }
                t1 = monotonicns64();
                if (t0 != t1) {
                    fps = 1e9 / (t1 - t0);
                }
                t0 = t1;
            } else {
                std::this_thread::sleep_for(std::chrono::milliseconds(1));
            }
        }
    }

    PIO pio = NULL;
    int sm = -1;
    std::span<typename colorspace::data_type const> framebuffer;
    bufseq_type buffers[3];
    buffer_manager manager{};
    matrix_geometry geometry;
    colorspace converter;
    std::thread blitter_thread;
    std::atomic<int> pending_error_errno;
};

} // namespace piomatter
