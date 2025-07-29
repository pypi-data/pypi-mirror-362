use std::arch::is_aarch64_feature_detected;
use encoding_rs::WINDOWS_1251;
// use encoding_rs::WINDOWS_1251;
use pyo3::prelude::*;

mod constants;
use constants::{A, C, PI, TAU};

#[cfg(feature = "simd")]
mod simd_impl {
    use super::*;

    // x86_64 SIMD реализации
    #[cfg(target_arch = "x86_64")]
    use std::arch::x86_64::*;

    #[cfg(target_arch = "x86_64")]
    pub unsafe fn transform_x_avx2(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        for i in (0..64).step_by(32) {
            let a_vec = _mm256_loadu_si256(a.as_ptr().add(i) as *const __m256i);
            let b_vec = _mm256_loadu_si256(b.as_ptr().add(i) as *const __m256i);
            let result_vec = _mm256_xor_si256(a_vec, b_vec);
            _mm256_storeu_si256(result.as_mut_ptr().add(i) as *mut __m256i, result_vec);
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub unsafe fn transform_x_sse2(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        for i in (0..64).step_by(16) {
            let a_vec = _mm_loadu_si128(a.as_ptr().add(i) as *const __m128i);
            let b_vec = _mm_loadu_si128(b.as_ptr().add(i) as *const __m128i);
            let result_vec = _mm_xor_si128(a_vec, b_vec);
            _mm_storeu_si128(result.as_mut_ptr().add(i) as *mut __m128i, result_vec);
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub fn transform_x_optimized(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        if is_x86_feature_detected!("avx2") {
            unsafe { transform_x_avx2(a, b, result) }
        } else if is_x86_feature_detected!("sse2") {
            unsafe { transform_x_sse2(a, b, result) }
        } else {
            transform_x_scalar(a, b, result)
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub unsafe fn add_512_sse2(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        let mut carry = 0u16;
        for i in (0..64).step_by(8).rev() {
            let mut temp_carry = carry;
            for j in (0..8).rev() {
                let idx = i + j;
                temp_carry = a[idx] as u16 + b[idx] as u16 + (temp_carry >> 8);
                result[idx] = temp_carry as u8;
            }
            carry = temp_carry >> 8;
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub fn add_512_optimized(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        if is_x86_feature_detected!("sse2") {
            unsafe { add_512_sse2(a, b, result) }
        } else {
            add_512_scalar(a, b, result)
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub unsafe fn transform_s_sse2(result: &mut [u8; 64]) {
        for i in (0..64).step_by(16) {
            unsafe {
                let data = _mm_loadu_si128(result.as_ptr().add(i) as *const __m128i);

                // Копируем SSE вектор в обычный массив
                let mut temp_array = [0u8; 16];
                _mm_storeu_si128(temp_array.as_mut_ptr() as *mut __m128i, data);

                // Применяем PI подстановку
                let mut substituted = [0u8; 16];
                for j in 0..16 {
                    substituted[j] = PI[temp_array[j] as usize];
                }

                // Загружаем обратно в SSE вектор
                let result_vec = _mm_loadu_si128(substituted.as_ptr() as *const __m128i);
                _mm_storeu_si128(result.as_mut_ptr().add(i) as *mut __m128i, result_vec);
            }
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub fn transform_s_optimized(result: &mut [u8; 64]) {
        if is_x86_feature_detected!("sse2") {
            unsafe { transform_s_sse2(result) }
        } else {
            transform_s_scalar(result)
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub unsafe fn transform_l_sse2(result: &mut [u8; 64]) {
        for i in 0..8 {
            let val = u64::from_be_bytes([
                result[i*8], result[i*8+1], result[i*8+2], result[i*8+3],
                result[i*8+4], result[i*8+5], result[i*8+6], result[i*8+7]
            ]);

            let mut res64 = 0u64;
            for j in 0..64 {
                if (val >> j) & 1 == 1 {
                    res64 ^= A[63 - j];
                }
            }

            let bytes = res64.to_be_bytes();
            result[i*8..(i+1)*8].copy_from_slice(&bytes);
        }
    }

    #[cfg(target_arch = "x86_64")]
    pub fn transform_l_optimized(result: &mut [u8; 64]) {
        if is_x86_feature_detected!("sse2") {
            unsafe { transform_l_sse2(result) }
        } else {
            transform_l_scalar(result)
        }
    }

    // ARM64 NEON реализации
    #[cfg(target_arch = "aarch64")]
    use std::arch::aarch64::*;

    #[cfg(target_arch = "aarch64")]
    #[target_feature(enable = "neon")]
    pub unsafe fn transform_x_neon(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        for i in (0..64).step_by(16) {
            unsafe {
                let a_vec = vld1q_u8(a.as_ptr().add(i));
                let b_vec = vld1q_u8(b.as_ptr().add(i));
                let result_vec = veorq_u8(a_vec, b_vec);
                vst1q_u8(result.as_mut_ptr().add(i), result_vec);
            }
        }
    }

    #[cfg(target_arch = "aarch64")]
    pub fn transform_x_optimized(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        if is_aarch64_feature_detected!("neon") {
            unsafe { transform_x_neon(a, b, result) }
        } else {
            transform_x_scalar(a, b, result)
        }
    }

    #[cfg(target_arch = "aarch64")]
    pub fn add_512_optimized(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        add_512_scalar(a, b, result)
    }

    #[cfg(target_arch = "aarch64")]
    #[target_feature(enable = "neon")]
    pub unsafe fn transform_s_neon(result: &mut [u8; 64]) {
        for i in (0..64).step_by(16) {
            unsafe {
                let data = vld1q_u8(result.as_ptr().add(i));

                // Копируем NEON вектор в обычный массив
                let mut temp_array = [0u8; 16];
                vst1q_u8(temp_array.as_mut_ptr(), data);

                // Применяем PI подстановку
                let mut substituted = [0u8; 16];
                for j in 0..16 {
                    substituted[j] = PI[temp_array[j] as usize];
                }

                // Загружаем обратно в NEON вектор
                let result_vec = vld1q_u8(substituted.as_ptr());
                vst1q_u8(result.as_mut_ptr().add(i), result_vec);
            }
        }
    }


    #[cfg(target_arch = "aarch64")]
    pub fn transform_s_optimized(result: &mut [u8; 64]) {
        if is_aarch64_feature_detected!("neon") {
            unsafe { transform_s_neon(result) }
        } else {
            transform_s_scalar(result)
        }
    }

    #[cfg(target_arch = "aarch64")]
    #[target_feature(enable = "neon")]
    pub unsafe fn transform_l_neon(result: &mut [u8; 64]) {
        for i in 0..8 {
            let val = u64::from_be_bytes([
                result[i*8], result[i*8+1], result[i*8+2], result[i*8+3],
                result[i*8+4], result[i*8+5], result[i*8+6], result[i*8+7]
            ]);

            let mut res64 = 0u64;
            for j in 0..64 {
                if (val >> j) & 1 == 1 {
                    res64 ^= A[63 - j];
                }
            }

            let bytes = res64.to_be_bytes();
            result[i*8..(i+1)*8].copy_from_slice(&bytes);
        }
    }

    #[cfg(target_arch = "aarch64")]
    pub fn transform_l_optimized(result: &mut [u8; 64]) {
        if is_aarch64_feature_detected!("neon") {
            unsafe { transform_l_neon(result) }
        } else {
            transform_l_scalar(result)
        }
    }

    // Fallback для других архитектур
    #[cfg(not(any(target_arch = "x86_64", target_arch = "aarch64")))]
    pub fn transform_x_optimized(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        transform_x_scalar(a, b, result)
    }

    #[cfg(not(any(target_arch = "x86_64", target_arch = "aarch64")))]
    pub fn add_512_optimized(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
        add_512_scalar(a, b, result)
    }

    #[cfg(not(any(target_arch = "x86_64", target_arch = "aarch64")))]
    pub fn transform_s_optimized(result: &mut [u8; 64]) {
        transform_s_scalar(result)
    }

    #[cfg(not(any(target_arch = "x86_64", target_arch = "aarch64")))]
    pub fn transform_l_optimized(result: &mut [u8; 64]) {
        transform_l_scalar(result)
    }
}

// Скалярные реализации (оригинальные)
fn add_512_scalar(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
    let mut temp: u16 = 0;
    for i in (0..64).rev() {
        temp = a[i] as u16 + b[i] as u16 + (temp >> 8);
        result[i] = temp as u8;
    }
}

fn transform_x_scalar(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
    for (index, byte) in result.iter_mut().enumerate() {
        *byte = a[index] ^ b[index];
    }
}

fn transform_s_scalar(result: &mut [u8; 64]) {
    result
        .iter_mut()
        .for_each(|byte| *byte = PI[*byte as usize]);
}

fn transform_p_scalar(result: &mut [u8; 64]) {
    let temp = result.clone();
    for (index, position) in TAU.iter().enumerate() {
        result[index] = temp[*position as usize];
    }
}

fn transform_l_scalar(result: &mut [u8; 64]) {
    let input_u64: [u64; 8] = result
        .chunks_exact(8)
        .map(|bytes| u64::from_be_bytes(bytes.try_into().unwrap()))
        .collect::<Vec<u64>>()
        .try_into()
        .unwrap();

    let mut buffers = [0u64; 8];

    for i in 0..8 {
        for j in 0..64 {
            if (input_u64[i] >> j) & 1 == 1 {
                buffers[i] ^= A[63 - j];
            }
        }
    }

    let buffer: [u8; 64] = buffers
        .iter()
        .flat_map(|bytes| bytes.to_be_bytes())
        .collect::<Vec<u8>>()
        .try_into()
        .unwrap();

    for (index, byte) in buffer.iter().enumerate() {
        result[index] = *byte;
    }
}

// Публичные функции с выбором оптимизации
fn add_512(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
    #[cfg(feature = "simd")]
    {
        simd_impl::add_512_optimized(a, b, result);
    }
    #[cfg(not(feature = "simd"))]
    {
        add_512_scalar(a, b, result);
    }
}

fn transform_x(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
    #[cfg(feature = "simd")]
    {
        simd_impl::transform_x_optimized(a, b, result);
    }
    #[cfg(not(feature = "simd"))]
    {
        transform_x_scalar(a, b, result);
    }
}

fn transform_s(result: &mut [u8; 64]) {
    #[cfg(feature = "simd")]
    {
        simd_impl::transform_s_optimized(result);
    }
    #[cfg(not(feature = "simd"))]
    {
        transform_s_scalar(result);
    }
}

fn transform_p(result: &mut [u8; 64]) {
    // P-преобразование сложно оптимизировать с SIMD из-за произвольных перестановок
    transform_p_scalar(result);
}

fn transform_l(result: &mut [u8; 64]) {
    #[cfg(feature = "simd")]
    {
        simd_impl::transform_l_optimized(result);
    }
    #[cfg(not(feature = "simd"))]
    {
        transform_l_scalar(result);
    }
}

fn key_schedule(keys: &mut [u8; 64], iter_index: usize) {
    transform_x(&keys.clone(), &C[iter_index], keys);
    transform_s(keys);
    transform_p(keys);
    transform_l(keys);
}

fn transform_e(keys: &mut [u8; 64], block: &[u8; 64], state: &mut [u8; 64]) {
    transform_x(block, keys, state);

    for i in 0..12 {
        transform_s(state);
        transform_p(state);
        transform_l(state);
        key_schedule(keys, i);
        transform_x(&state.clone(), keys, state);
    }
}

fn transform_g(n: &[u8; 64], hash: &mut [u8; 64], message: &[u8; 64]) {
    let mut keys = [0u8; 64];
    let mut temp = [0u8; 64];

    transform_x(n, hash, &mut keys);

    transform_s(&mut keys);
    transform_p(&mut keys);
    transform_l(&mut keys);

    transform_e(&mut keys, message, &mut temp);

    transform_x(&temp.clone(), hash, &mut temp);
    transform_x(&temp, message, hash);
}

fn streebog_core(message: &[u8], hash: &mut [u8; 64]) {
    let mut n = [0u8; 64];
    let mut sigma = [0u8; 64];
    let mut block_size = [0u8; 64];

    if message.is_empty() {
        // Специальная обработка пустого сообщения
        let mut block = [0u8; 64];
        block[0] = 1;  // Padding для пустого блока
        block.reverse();

        // Размер блока = 0 для пустого сообщения
        let empty_size = [0u8; 64];

        transform_g(&n, hash, &block);
        add_512(&n.clone(), &empty_size, &mut n);
        add_512(&sigma.clone(), &block, &mut sigma);
    } else {
        // Обработка непустых сообщений (ваш текущий код)
        for chunk in message.chunks(64) {
            let chunk_size = chunk.len() as u16 * 8;
            block_size[62..].copy_from_slice(&chunk_size.to_be_bytes());

            let mut block = [0u8; 64];
            if chunk.len() < 64 {
                block[..chunk.len()].copy_from_slice(chunk);
                block[chunk.len()] = 1;
            } else {
                block.copy_from_slice(chunk);
            }
            block.reverse();

            transform_g(&n, hash, &block);
            add_512(&n.clone(), &block_size, &mut n);
            add_512(&sigma.clone(), &block, &mut sigma);
        }

        // Добавляем padding блок для кратных 64 байтам
        if message.len() % 64 == 0 {
            let mut padding_block = [0u8; 64];
            padding_block[0] = 1;
            padding_block.reverse();

            let padding_size = [0u8; 64];

            transform_g(&n, hash, &padding_block);
            add_512(&n.clone(), &padding_size, &mut n);
            add_512(&sigma.clone(), &padding_block, &mut sigma);
        }
    }

    transform_g(&[0u8; 64], hash, &n);
    transform_g(&[0u8; 64], hash, &sigma);
    hash.reverse();
}



#[pyfunction]
pub fn streebog_512(message: &[u8]) -> PyResult<String> {
    let mut hash = [0u8; 64];
    streebog_core(message, &mut hash);
    Ok(hex::encode(hash))
}

#[pyfunction]
pub fn streebog_256(message: &[u8]) -> PyResult<String> {
    let mut hash = [1u8; 64];
    streebog_core(message, &mut hash);
    Ok(hex::encode(&hash[32..]))
}

#[pyclass]
pub struct HashFieldsAdapter;

#[pymethods]
impl HashFieldsAdapter {
    #[new]
    fn new() -> Self {
        HashFieldsAdapter
    }

    fn hash_field_256(&self, field_content: &str) -> PyResult<String> {
        let (encoded_bytes, _, _) = WINDOWS_1251.encode(field_content);
        // let encoded_bytes = field_content.as_bytes();
        let mut hash = [1u8; 64];
        streebog_core(&encoded_bytes, &mut hash);
        Ok(hex::encode(&hash[32..]))
    }

    fn hash_field_512(&self, field_content: &str) -> PyResult<String> {
        let (encoded_bytes, _, _) = WINDOWS_1251.encode(field_content);
        // let encoded_bytes = field_content.as_bytes();
        let mut hash = [0u8; 64];
        streebog_core(&encoded_bytes, &mut hash);
        Ok(hex::encode(hash))
    }
}

#[pyfunction]
pub fn simd_info() -> PyResult<String> {
    let mut info = Vec::new();

    // Проверка compile-time features
    #[cfg(feature = "simd")]
    info.push("SIMD feature: enabled".to_string());

    #[cfg(not(feature = "simd"))]
    info.push("SIMD feature: disabled".to_string());

    // Проверка архитектуры
    info.push(format!("Architecture: {}", std::env::consts::ARCH));

    // Проверка runtime поддержки для x86_64
    #[cfg(all(feature = "simd", target_arch = "x86_64"))]
    {
        if is_x86_feature_detected!("avx2") {
            info.push("AVX2: supported".to_string());
        } else {
            info.push("AVX2: not supported".to_string());
        }

        if is_x86_feature_detected!("sse2") {
            info.push("SSE2: supported".to_string());
        } else {
            info.push("SSE2: not supported".to_string());
        }
    }

    // Проверка runtime поддержки для ARM64
    #[cfg(all(feature = "simd", target_arch = "aarch64"))]
    {
        if is_aarch64_feature_detected!("neon") {
            info.push("NEON: supported".to_string());
        } else {
            info.push("NEON: not supported".to_string());
        }
    }

    Ok(info.join("\n"))
}

#[pymodule]
#[pyo3(name = "streebog_rs")]
fn register(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(streebog_256, m)?)?;
    m.add_function(wrap_pyfunction!(streebog_512, m)?)?;
    m.add_class::<HashFieldsAdapter>()?;
    m.add_function(wrap_pyfunction!(simd_info, m)?)?;
    Ok(())
}
