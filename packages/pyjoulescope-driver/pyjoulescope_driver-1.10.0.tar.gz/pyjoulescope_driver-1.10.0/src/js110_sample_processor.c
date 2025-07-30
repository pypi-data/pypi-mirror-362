/*
 * Copyright 2018-2022 Jetperch LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "jsdrv_prv/js110_sample_processor.h"
#include "jsdrv/error_code.h"
#include <string.h>
#include <float.h>
#include <math.h>

#define _SUPPRESS_SAMPLES_MASK (JS110_SUPPRESS_SAMPLES_MAX - 1)
#define SUPPRESS_WINDOW_MAX 12
#define SUPPRESS_PRE_MAX 8
#define SUPPRESS_POST_MAX 8


static inline uint8_t ptr_incr(uint8_t idx) {
    return (idx + 1) & _SUPPRESS_SAMPLES_MASK;
}

static inline uint8_t ptr_decr(uint8_t idx) {
    return (idx - 1) & _SUPPRESS_SAMPLES_MASK;
}

static inline uint8_t ptr_sub(uint8_t a, uint8_t b) {
    return (a - b) & _SUPPRESS_SAMPLES_MASK;
}

static struct js110_sample_s SAMPLE_MISSING = {
        .i = 0.0f,  // initialized to NAN
        .v = 0.0f,  // initialized to NAN
        .p = 0.0f,  // initialized to NAN
        .current_range = JS110_I_RANGE_MISSING,
        .gpi0 = 0,
        .gpi1 = 0,
};


// experimentally determined charge coupling durations in samples at 2 MSPS
// These values are aggressive and result in min/max distortion
static const uint8_t SUPPRESS_MATRIX_M[9][9] = {   // [to][from]
    //0, 1, 2, 3, 4, 5, 6, 7, 8   # from this current select
    {0, 5, 5, 5, 5, 5, 6, 6, 0},  // to 0
    {3, 0, 5, 5, 5, 6, 7, 8, 0},  // to 1
    {4, 4, 0, 6, 6, 7, 7, 8, 0},  // to 2
    {4, 4, 4, 0, 6, 6, 7, 7, 0},  // to 3
    {4, 4, 4, 4, 0, 6, 7, 6, 0},  // to 4
    {4, 4, 4, 4, 4, 0, 7, 6, 0},  // to 5
    {4, 4, 4, 4, 4, 4, 0, 6, 0},  // to 6
    {0, 0, 0, 0, 0, 0, 0, 0, 0},  // to 7 (off)
    {0, 0, 0, 0, 0, 0, 0, 0, 0},  // to 8 (missing)
};

// experimentally determined charge coupling durations in samples at 2 MSPS
// These values are more conservative for less min/max distortion.
static const uint8_t SUPPRESS_MATRIX_N[9][9] = {   // [to][from]
    //0, 1, 2, 3, 4, 5, 6, 7, 8   // from this current select
    {0, 5, 7, 7, 7, 7, 7, 8, 0},  // to 0
    {3, 0, 7, 7, 7, 7, 7, 8, 0},  // to 1
    {5, 5, 0, 7, 7, 7, 7, 8, 0},  // to 2
    {5, 5, 5, 0, 7, 7, 7, 8, 0},  // to 3
    {5, 5, 5, 5, 0, 7, 7, 8, 0},  // to 4
    {5, 5, 5, 5, 5, 0, 7, 8, 0},  // to 5
    {5, 5, 5, 5, 5, 5, 0, 8, 0},  // to 6
    {0, 0, 0, 0, 0, 0, 0, 0, 0},  // to 7 (off)
    {0, 0, 0, 0, 0, 0, 0, 0, 0},  // to 8 (missing)
};

void js110_sp_initialize(struct js110_sp_s * self) {
    memset(self, 0, sizeof(*self));
    self->_suppress_samples_pre = 1;
    self->_suppress_samples_window = 10;
    self->_suppress_samples_post = 1;
    self->_suppress_mode = JS110_SUPPRESS_MODE_INTERP;
    self->_suppress_matrix = &SUPPRESS_MATRIX_N;
    SAMPLE_MISSING.i = NAN;
    SAMPLE_MISSING.v = NAN;
    SAMPLE_MISSING.p = NAN;
    js110_sp_reset(self);
}

void js110_sp_reset(struct js110_sp_s * self) {
    self->sample_missing_count = 0;
    self->is_skipping = 1;
    self->skip_count = 0;
    self->sample_sync_count = 0;
    self->contiguous_count = 0;
    self->sample_count = 0;

    self->_suppress_samples_remaining = 0;
    self->_suppress_samples_counter = 0;
    self->_i_range_last = JS110_I_RANGE_OFF;

    self->_voltage_range = 0;
    self->_idx_out = 0;
    self->_idx_suppress_start = 0;

    for (uint32_t idx = 0; idx < JS110_SUPPRESS_SAMPLES_MAX; ++idx) {
        self->samples[idx] = SAMPLE_MISSING;
    }
}

struct js110_sample_s js110_sp_process(struct js110_sp_s * self, uint32_t sample_u32, uint8_t v_range) {
    struct js110_sample_s s;
    ++self->sample_count;

    // interpret sample_u32 and apply calibration
    uint8_t i_range = (sample_u32 & 3) | (((sample_u32 >> 16) & 1) << 2);
    if ((i_range > 7) || (sample_u32 == 0xffffffffLU)) {
        ++self->sample_missing_count;
        self->contiguous_count = 0;
        if (self->is_skipping == 0) {
            ++self->skip_count;
            self->is_skipping = 1;
        }
        s = SAMPLE_MISSING;
    } else {
        ++self->contiguous_count;
        self->is_skipping = 0;
        double i = (double) ((sample_u32 >> 2) & 0x3fff);
        double v = (double) ((sample_u32 >> 18) & 0x3fff);
        i = (i + self->cal[0][0][i_range]) * self->cal[0][1][i_range];
        v = (v + self->cal[1][0][v_range]) * self->cal[1][1][v_range];
        s.i = (float) i;
        s.v = (float) v;
        s.p = (float) (i * v);
        s.current_range = i_range;
        s.gpi0 = (sample_u32 >> 2) & 1;
        s.gpi1 = (sample_u32 >> 18) & 1;
    }

    if ((self->_i_range_last != i_range) && (self->_i_range_last != JS110_I_RANGE_MISSING)) {
        uint8_t suppress_window;
        if (self->_suppress_matrix != NULL) {
            suppress_window = self->_suppress_matrix[0][i_range][self->_i_range_last];
        } else {
            suppress_window = self->_suppress_samples_window;
        }
        self->_suppress_samples_counter = suppress_window;
        if (suppress_window) {
            if (0 == self->_suppress_samples_remaining) {
                self->start = self->head;
            }
            self->_suppress_samples_remaining = suppress_window + self->_suppress_samples_post;
        }
    }

    if ((self->_suppress_mode == JS110_SUPPRESS_MODE_NAN) && (self->_suppress_samples_counter)) {
        s.i = NAN;
        s.v = NAN;
        s.p = NAN;
        --self->_suppress_samples_counter;
    }

    self->samples[self->head] = s;
    self->head = ptr_incr(self->head);

    if (self->_suppress_samples_remaining) {
        ++self->_suppress_samples_counter;
        --self->_suppress_samples_remaining;
        if (0 == self->_suppress_samples_remaining) {
            if (self->_suppress_mode == JS110_SUPPRESS_MODE_MEAN) {
                uint32_t sample_count = 0;
                double accum = 0.0f;
                uint8_t ptr = self->start;
                if (self->_i_range_last < 7) {
                    for (int32_t k = 0; k < self->_suppress_samples_pre; ++k) {
                        ptr = ptr_decr(ptr);
                        accum += self->samples[ptr].i;
                    }
                    sample_count += self->_suppress_samples_pre;
                }

                uint8_t ptr_end = self->head;
                for (int32_t k = 0; k < self->_suppress_samples_post; ++k) {
                    ptr_end = ptr_decr(ptr_end);
                    accum += self->samples[ptr_end].i;
                }
                sample_count += self->_suppress_samples_post;

                accum /= sample_count;
                float mean = (float) accum;
                ptr = self->start;
                while (ptr != ptr_end) {
                    self->samples[ptr].i = mean;
                    self->samples[ptr].p = self->samples[ptr].i * self->samples[ptr].v;
                    ptr = ptr_incr(ptr);
                }
            } else if (self->_suppress_mode == JS110_SUPPRESS_MODE_INTERP) {
                double pre = 0.0f;
                double post = 0.0f;
                uint8_t ptr = self->start;
                for (int32_t k = 0; k < self->_suppress_samples_pre; ++k) {
                    ptr = ptr_decr(ptr);
                    pre += self->samples[ptr].i;
                }
                pre /= self->_suppress_samples_pre;

                uint8_t ptr_end = self->head;
                for (int32_t k = 0; k < self->_suppress_samples_post; ++k) {
                    ptr_end = ptr_decr(ptr_end);
                    post += self->samples[ptr_end].i;
                }
                post /= self->_suppress_samples_post;
                if (self->_i_range_last >= 7) {
                    pre = post;
                }
                uint8_t count = ptr_end - ptr;
                double step = 0.0;
                if (count) {
                    step = (post - pre) / count;
                }

                ptr = self->start;
                int32_t k = 0;
                while (ptr != ptr_end) {
                    self->samples[ptr].i = (float) (pre + (step * (k + 1)));
                    self->samples[ptr].p = self->samples[ptr].i * self->samples[ptr].v;
                    ptr = ptr_incr(ptr);
                    ++k;
                }
            }
        }
    }

    self->_i_range_last = i_range;
    return self->samples[self->head];
}

int32_t js110_sp_suppress_win(struct js110_sp_s * self, uint8_t window) {
    switch (window) {
        case 0: self->_suppress_matrix = NULL; break;
        case 1: self->_suppress_matrix = &SUPPRESS_MATRIX_M; break;
        case 2: self->_suppress_matrix = &SUPPRESS_MATRIX_N; break;
        default: return JSDRV_ERROR_PARAMETER_INVALID;
    }
    return 0;
}