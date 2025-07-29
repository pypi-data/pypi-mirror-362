use encoding_rs::WINDOWS_1251;
use pyo3::prelude::*;

mod constants;
use constants::{A, C, PI, TAU};

fn add_512(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
    let mut temp: u16 = 0;
    for i in (0..64).rev() {
        temp = a[i] as u16 + b[i] as u16 + (temp >> 8);
        result[i] = temp as u8;
    }
}

fn transform_x(a: &[u8; 64], b: &[u8; 64], result: &mut [u8; 64]) {
    for (index, byte) in result.iter_mut().enumerate() {
        *byte = a[index] ^ b[index];
    }
}

fn transform_s(result: &mut [u8; 64]) {
    result
        .iter_mut()
        .for_each(|byte| *byte = PI[*byte as usize]);
}

fn transform_p(result: &mut [u8; 64]) {
    let temp = result.clone();
    for (index, position) in TAU.iter().enumerate() {
        result[index] = temp[*position as usize];
    }
}

fn transform_l(result: &mut [u8; 64]) {
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
    let mut block: [u8; 64];

    for chunk in message.chunks(64) {
        let chunk_size = chunk.len() as u16 * 8;
        block_size[62..].copy_from_slice(&chunk_size.to_be_bytes());

        if chunk.len() != 64 {
            block = [0u8; 64];
            block[..chunk.len()].copy_from_slice(chunk);
            block[chunk.len()] = 1;
        } else {
            block = chunk.try_into().unwrap();
        }
        block.reverse();

        transform_g(&n, hash, &block);
        add_512(&n.clone(), &block_size, &mut n);
        add_512(&sigma.clone(), &block, &mut sigma);
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
        let mut hash = [1u8; 64];
        streebog_core(&encoded_bytes, &mut hash);
        Ok(hex::encode(&hash[32..]))
    }

    fn hash_field_512(&self, field_content: &str) -> PyResult<String> {
        let (encoded_bytes, _, _) = WINDOWS_1251.encode(field_content);
        let mut hash = [0u8; 64];
        streebog_core(&encoded_bytes, &mut hash);
        Ok(hex::encode(hash))
    }
}

#[pymodule]
#[pyo3(name = "streebog_rs")]
fn register(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(streebog_256, m)?)?;
    m.add_function(wrap_pyfunction!(streebog_512, m)?)?;
    m.add_class::<HashFieldsAdapter>()?;
    Ok(())
}
