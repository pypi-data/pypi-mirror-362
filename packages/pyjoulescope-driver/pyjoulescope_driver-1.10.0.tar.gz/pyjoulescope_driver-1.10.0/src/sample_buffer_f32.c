/*
 * Copyright 2022 Jetperch LLC
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

#include "jsdrv_prv/sample_buffer_f32.h"
#include "jsdrv_prv/platform.h"
#include "jsdrv_prv/cdef.h"
#include <math.h>


JSDRV_STATIC_ASSERT(offsetof(struct sbuf_f32_s, msg_sample_id) + 4 == offsetof(struct sbuf_f32_s, buffer), sample_id_location);


void sbuf_f32_clear(struct sbuf_f32_s * self) {
    if (NULL != self) {
        jsdrv_memset(self, 0, offsetof(struct sbuf_f32_s, buffer));
        self->sample_id_decimate = 2;
    }
}

uint32_t sbuf_f32_length(struct sbuf_f32_s * self) {
    return (self->head - self->tail) & SAMPLE_BUFFER_MASK;
}

uint64_t sbuf_head_sample_id(struct sbuf_f32_s * self) {
    return self->head_sample_id;
}

uint64_t sbuf_tail_sample_id(struct sbuf_f32_s * self) {
    return self->head_sample_id - sbuf_f32_length(self) * self->sample_id_decimate;
}

void sbuf_f32_add(struct sbuf_f32_s * self, uint64_t sample_id, float * data, uint32_t length) {
    if (NULL == self) {
        return;
    }
    if (self->head_sample_id > sample_id) {
        // common case, some overlap with previous data, only need new data.
        uint64_t dup = (self->head_sample_id - sample_id) / self->sample_id_decimate;
        if (dup >= length) {
            return;
        }
        data += dup;
        length -= (uint32_t) dup;
        sample_id += dup * self->sample_id_decimate;
    }
    if (length >= SAMPLE_BUFFER_LENGTH) {
        // uncommon case, incoming data is larger than our buffer
        uint32_t skip = length - (SAMPLE_BUFFER_LENGTH - 1);
        data += skip;
        length = SAMPLE_BUFFER_LENGTH - 1;
        self->head_sample_id = sample_id - length * self->sample_id_decimate;
    } else if (self->head_sample_id < sample_id) {
        // uncommon case, missing samples, fill with NaN
        uint64_t skips = (sample_id - self->head_sample_id) / self->sample_id_decimate;
        if (skips >= (SAMPLE_BUFFER_LENGTH - 1)) {
            skips = SAMPLE_BUFFER_LENGTH - 1;
            self->head_sample_id = sample_id - skips * self->sample_id_decimate;
            self->tail = self->head;
        }
        while (self->head_sample_id < sample_id) {
            self->buffer[self->head] = NAN;
            self->head = (self->head + 1) & SAMPLE_BUFFER_MASK;
            if (self->tail == self->head) {
                self->tail = (self->tail + 1) & SAMPLE_BUFFER_MASK;
            }
            self->head_sample_id += self->sample_id_decimate;
        }
    }

    // Copy new data to buffer
    self->head_sample_id += length * self->sample_id_decimate;
    while (length) {
        self->buffer[self->head] = *data++;
        self->head = (self->head + 1) & SAMPLE_BUFFER_MASK;
        if (self->tail == self->head) {
            self->tail = (self->tail + 1) & SAMPLE_BUFFER_MASK;
        }
        --length;
    }
}

void sbuf_f32_advance(struct sbuf_f32_s * self, uint64_t sample_id) {
    uint64_t self_sample_id = sbuf_tail_sample_id(self);
    if (self_sample_id < sample_id) {
        uint64_t delta_sample_id = sample_id - self_sample_id;
        uint64_t delta_count = delta_sample_id / self->sample_id_decimate;
        if (delta_count >= sbuf_f32_length(self)) {
            self->tail = self->head;
            self->head_sample_id = sample_id;
        } else {
            self->tail = (self->tail + delta_count) & SAMPLE_BUFFER_MASK;
        }
    }
}

void sbuf_f32_mult(struct sbuf_f32_s * r, struct sbuf_f32_s * s1, struct sbuf_f32_s * s2) {
    uint64_t r_sample_id = r->head_sample_id; // from last mult
    sbuf_f32_clear(r);
    r->sample_id_decimate = s1->sample_id_decimate;
    uint64_t s1_sample_id = sbuf_tail_sample_id(s1);
    if (r_sample_id < s1_sample_id) {
        r_sample_id = s1_sample_id;
    }
    uint64_t s2_sample_id = sbuf_tail_sample_id(s2);
    if (r_sample_id < s2_sample_id) {
        r_sample_id = s2_sample_id;
    }
    sbuf_f32_advance(s1, r_sample_id);
    sbuf_f32_advance(s2, r_sample_id);

    r->msg_sample_id = (uint32_t) (r_sample_id & 0xffffffff);
    r->head_sample_id = r_sample_id;
    while ((s1->tail != s1->head) && (s2->tail != s2->head)) {
        r->buffer[r->head++] = s1->buffer[s1->tail] * s2->buffer[s2->tail];
        s1->tail = (s1->tail + 1) & SAMPLE_BUFFER_MASK;
        s2->tail = (s2->tail + 1) & SAMPLE_BUFFER_MASK;
        r->head_sample_id += r->sample_id_decimate;
    }
}
