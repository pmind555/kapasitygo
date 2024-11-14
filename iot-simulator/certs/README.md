
# Certificate Generation for Devices

This folder contains the certificates required for secure communication between IoT devices and the backend. Below, we provide instructions for generating the necessary certificates using OpenSSL.

## Table of Contents
- [Root Certificate Authority (CA) Setup](#root-certificate-authority-ca-setup)
- [Device Certificates Generation](#device-certificates-generation)
- [Important Notes](#important-notes)

## Root Certificate Authority (CA) Setup

First, create a root Certificate Authority (CA) which will be used to sign device certificates.

1. **Generate the Root CA Key**:
   ```bash
   openssl genrsa -out rootCA.key 2048
   ```
   This command generates a 2048-bit RSA private key for the Root CA.

2. **Create the Root CA Certificate**:
   ```bash
   openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.pem
   ```
   This command generates a self-signed certificate (`rootCA.pem`) that is valid for 10 years (`3650` days). You will be prompted to enter details such as the "Common Name" for the CA.

## Device Certificates Generation

For each device, we generate a private key, create a Certificate Signing Request (CSR), and then sign the CSR using the Root CA.

### Steps to Generate Device Certificates

1. **Generate a Private Key for the Device**:
   - For example, for `device1`:
     ```bash
     openssl genrsa -out device1.key 2048
     ```
     This command generates a 2048-bit RSA private key for the device.

2. **Create a Certificate Signing Request (CSR)**:
   - For `device1`, create the CSR:
     ```bash
     openssl req -new -key device1.key -out device1.csr
     ```
     You will be prompted to enter details like the "Common Name". **Important:** The "Common Name" should be the `device_id` from the database. This uniquely identifies the device.

3. **Sign the CSR with the Root CA to Create the Device Certificate**:
   - Use the Root CA to sign the CSR and create the `.crt` file:
     ```bash
     openssl x509 -req -in device1.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device1.crt -days 365 -sha256
     ```
     This command creates a signed certificate (`device1.crt`) valid for 1 year.

### Examples for Other Devices

Here are commands used for other devices:

- **Generate Key and CSR for Device `429b1945-2b3a-44ca-8fc7-5b19e3ddb96f`**:
  ```bash
  openssl genrsa -out 429b1945-2b3a-44ca-8fc7-5b19e3ddb96f.key 2048
  openssl req -new -key 429b1945-2b3a-44ca-8fc7-5b19e3ddb96f.key -out 429b1945-2b3a-44ca-8fc7-5b19e3ddb96f.csr
  ```

- **Sign the CSR for Device `429b1945-2b3a-44ca-8fc7-5b19e3ddb96f`**:
  ```bash
  openssl x509 -req -in 429b1945-2b3a-44ca-8fc7-5b19e3ddb96f.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out 429b1945-2b3a-44ca-8fc7-5b19e3ddb96f.crt -days 365 -sha256
  ```

## Important Notes

1. **Common Name (CN) Usage**:
   - When generating the CSR for each device, make sure to set the **"Common Name (CN)"** to the `device_id` from the database. This ensures the certificate can uniquely identify the device.

2. **File Descriptions**:
   - **`rootCA.key`**: Private key for the Root Certificate Authority.
   - **`rootCA.pem`**: Self-signed certificate for the Root CA.
   - **`deviceX.key`**: Private key for the individual device.
   - **`deviceX.csr`**: Certificate Signing Request for the device.
   - **`deviceX.crt`**: Certificate for the device, signed by the Root CA.

3. **Certificate Validity**:
   - The Root CA certificate is valid for **10 years**.
   - Each device certificate is valid for **1 year**.

4. **Security**:
   - Keep private keys (`.key` files) secure. They should not be shared publicly.

5. **Certificate Revocation**:
   - If a device is compromised, the corresponding certificate should be revoked, and a new certificate should be generated.

Feel free to refer to this guide whenever you need to create or renew certificates for the devices in the system.

