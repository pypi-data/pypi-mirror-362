
fn wrap_pkcs7(data: &[u8]) -> Vec<u8> {
    let wrap: [u8; 13] = [
        0x06, 0x09,
        0x2a, 0x86, 0x48, 0x86, 0xf7, 0x0d, 0x01, 0x07, 0x02,
        0xa0, 0x82,
    ];

    if data.len() >= 17 && &data[4..17] == wrap {
        return data.to_vec();
    }

    let mut ret = vec![0x30, 0x82];
    let data_len_plus_15 = (data.len() + 15) as u16;
    ret.extend_from_slice(&data_len_plus_15.to_be_bytes());
    ret.extend_from_slice(&wrap);
    let data_len = data.len() as u16;
    ret.extend_from_slice(&data_len.to_be_bytes());
    ret.extend_from_slice(data);
    ret
}

fn main() {
    // Example usage with a dummy data slice.
    // In a real scenario, you would replace this with your actual data.
    let data = b"some pkcs7 data";
    let wrapped_data = wrap_pkcs7(data);
    println!("{:x?}", wrapped_data);
}
