// IMPORT
use ripemd::{Digest, Ripemd128, Ripemd160, Ripemd256, Ripemd320};
use blake3 as blakethree;
use pyo3::prelude::*;

// MAIN
#[pyclass]
pub struct BLAKE3 {
    hasher: blakethree::Hasher
}

#[pymethods]
impl BLAKE3 {
    #[new]
    fn new() -> Self {
        BLAKE3 {
            hasher: blakethree::Hasher::new()
        }
    }
    //
    fn update(&mut self, buffer: Vec<u8>) -> PyResult<()> {
        self.hasher.update(&buffer);
        Ok(())
    }
    //
    fn digest(&self) -> PyResult<Vec<u8>> {
        let result = self.hasher.finalize().as_bytes().to_vec();
        Ok(result)
    }
    //
    fn extend(&self, length: usize) -> PyResult<Vec<u8>> {
        let mut result = vec![0u8; length];
        let mut xof = self.hasher.finalize_xof();
        xof.fill(&mut result);
        Ok(result)
    }
}

#[pyclass]
pub struct RIPEMD128 {
    hasher: Ripemd128
}

#[pymethods]
impl RIPEMD128 {
    #[new]
    fn new() -> Self {
        RIPEMD128 {
            hasher: Ripemd128::new()
        }
    }
    //
    fn update(&mut self, buffer: Vec<u8>) -> PyResult<()> {
        self.hasher.update(&buffer);
        Ok(())
    }
    //
    fn digest(&self) -> PyResult<Vec<u8>> {
        let mut copy = self.hasher.clone();
        let result = copy.finalize_reset().to_vec();
        Ok(result)
    }
    //
    fn reset(&mut self) -> PyResult<()> {
        self.hasher.reset();
        Ok(())
    }
}

#[pyclass]
pub struct RIPEMD160 {
    hasher: Ripemd160
}

#[pymethods]
impl RIPEMD160 {
    #[new]
    fn new() -> Self {
        RIPEMD160 {
            hasher: Ripemd160::new()
        }
    }
    //
    fn update(&mut self, buffer: Vec<u8>) -> PyResult<()> {
        self.hasher.update(&buffer);
        Ok(())
    }
    //
    fn digest(&self) -> PyResult<Vec<u8>> {
        let mut copy = self.hasher.clone();
        let result = copy.finalize_reset().to_vec();
        Ok(result)
    }
    //
    fn reset(&mut self) -> PyResult<()> {
        self.hasher.reset();
        Ok(())
    }
}

#[pyclass]
pub struct RIPEMD256 {
    hasher: Ripemd256
}

#[pymethods]
impl RIPEMD256 {
    #[new]
    fn new() -> Self {
        RIPEMD256 {
            hasher: Ripemd256::new()
        }
    }
    //
    fn update(&mut self, buffer: Vec<u8>) -> PyResult<()> {
        self.hasher.update(&buffer);
        Ok(())
    }
    //
    fn digest(&self) -> PyResult<Vec<u8>> {
        let mut copy = self.hasher.clone();
        let result = copy.finalize_reset().to_vec();
        Ok(result)
    }
    //
    fn reset(&mut self) -> PyResult<()> {
        self.hasher.reset();
        Ok(())
    }
}

#[pyclass]
pub struct RIPEMD320 {
    hasher: Ripemd320
}

#[pymethods]
impl RIPEMD320 {
    #[new]
    fn new() -> Self {
        RIPEMD320 {
            hasher: Ripemd320::new()
        }
    }
    //
    fn update(&mut self, buffer: Vec<u8>) -> PyResult<()> {
        self.hasher.update(&buffer);
        Ok(())
    }
    //
    fn digest(&self) -> PyResult<Vec<u8>> {
        let mut copy = self.hasher.clone();
        let result = copy.finalize_reset().to_vec();
        Ok(result)
    }
    //
    fn reset(&mut self) -> PyResult<()> {
        self.hasher.reset();
        Ok(())
    }
}
