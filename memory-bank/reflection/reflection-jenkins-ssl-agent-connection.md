# Reflection: Jenkins Agent-Server SSL Connection (Self-Signed Cert)

## Context
This document summarizes the steps and lessons learned from troubleshooting and successfully connecting a Jenkins agent to a Jenkins server over HTTPS using a self-signed certificate, ensuring the process is repeatable after a reboot or server/agent shutdown.

---

## 1. Certificate and Nginx Setup

### a. Ensure Certificate Matches Domain
- The SSL certificate **must** have the correct Common Name (CN) and Subject Alternative Name (SAN) for your Jenkins server domain (e.g., `nisoservice.duckdns.org`).
- **Do not** use an IP address in the CN or SAN for a domain-based connection.

### b. Example OpenSSL Config (`jenkins-openssl.cnf`)
```ini
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
req_extensions     = req_ext
x509_extensions    = v3_req
prompt             = no

[ req_distinguished_name ]
C  = US
ST = State
L  = City
O  = Organization
CN = nisoservice.duckdns.org

[ req_ext ]
subjectAltName = @alt_names

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = nisoservice.duckdns.org
```

### c. Generate Key and Certificate (as root or with sudo)
```sh
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/jenkins-selfsigned.key \
  -out /etc/ssl/certs/jenkins-selfsigned.crt \
  -config /home/ubuntu/jenkins-openssl.cnf
```

### d. Update Nginx Config
In your SSL server block:
```nginx
ssl_certificate /etc/ssl/certs/jenkins-selfsigned.crt;
ssl_certificate_key /etc/ssl/private/jenkins-selfsigned.key;
```

### e. Test and Reload Nginx
```sh
sudo nginx -t
sudo systemctl reload nginx
```

---

## 2. Verifying Certificate
- Check that the certificate is served and matches the domain:
```sh
openssl s_client -connect nisoservice.duckdns.org:443 -servername nisoservice.duckdns.org
```
- Look for `Subject Alternative Name: DNS:nisoservice.duckdns.org` in the output.

---

## 3. Jenkins Agent Connection

### a. Download and Run Agent
```sh
curl -sO https://nisoservice.duckdns.org/jnlpJars/agent.jar
java -jar agent.jar -url https://nisoservice.duckdns.org/ -secret <your-secret> -name "first-agent" -webSocket -workDir "/home/ubuntu/jenkins" -noCertificateCheck
```
- The `-noCertificateCheck` flag is required for self-signed certs.
- Replace `<your-secret>` with the actual agent secret from Jenkins.

---

## 4. After Reboot (Agent or Server)

### On Jenkins Server:
1. **Start Jenkins and Nginx:**
   ```sh
   sudo systemctl start jenkins
   sudo systemctl start nginx
   ```
2. **(If needed) Re-issue certificate** if expired, using the steps above.

### On Jenkins Agent:
1. **SSH into the agent machine:**
   ```sh
   ssh -i <agent-key.pem> ubuntu@<agent-ip-address>
   ```
2. **Start the agent:**
   ```sh
   cd /home/ubuntu
   curl -sO https://nisoservice.duckdns.org/jnlpJars/agent.jar
   java -jar agent.jar -url https://nisoservice.duckdns.org/ -secret <your-secret> -name "first-agent" -webSocket -workDir "/home/ubuntu/jenkins" -noCertificateCheck &
   ```
   (The `&` runs it in the background. Use `nohup` if you want it to persist after logout.)

---

## 5. Troubleshooting Checklist
- If Nginx fails to reload, check:
  - Certificate and key paths
  - Permissions (`sudo chown root:www-data` and `chmod 640` for the key)
  - That the key and certificate match (use `openssl ... | openssl md5`)
- If agent fails to connect:
  - Check certificate SAN and CN
  - Use `-noCertificateCheck` for self-signed certs
  - Ensure Jenkins server is running and accessible

---

## 6. Recommendations
- Consider using Let's Encrypt for a trusted certificate (removes need for `-noCertificateCheck`).
- Document and store your OpenSSL config and commands for future use.
- Set reminders to renew your certificate before it expires.

---

**With these steps, you can quickly restore Jenkins agent-server connectivity after any reboot or shutdown, without repeating the full troubleshooting process.** 