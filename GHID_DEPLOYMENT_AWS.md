# Ghid Deployment AWS: Metal List pe EC2 + S3

**Stack Tehnologic:**
- EC2 t2.micro (GRATUIT - 750 ore/lună)
- S3 bucket (GRATUIT - 5GB stocare + transferuri)
- SQLite (local pe EC2)
- FastAPI + React

**Cost:** $0/lună (forever free tier)

**Timp până la deployment:** ~2 ore

---

## Cerințe Preliminare

Înainte de a începe, asigură-te că ai:
- ✅ Cont AWS (poți să te loghezi)
- ✅ Git (pentru push-ul codului)
- ✅ SSH key pair (sau dorință să creezi una)
- ✅ Nume de domeniu (opțional, ~$10/an)

---

## Partea 1: Configurare AWS Account & Servicii

### Pasul 1.1: Creează IAM User (Security Best Practice)

**De ce:** Nu folosi contul root. Creează un utilizator non-root pentru deploymente.

1. Mergi la AWS Console: https://console.aws.amazon.com/
2. Caută **IAM** → Click pe IAM
3. Sidebar stâng → **Users** → **Create user**
4. Nume: `metal-list-deployer`
5. Check: ✅ "Provide user access to AWS Management Console"
6. Setează parolă, click **Next**
7. Attach policy: Caută **AdministratorAccess** → Bifează
8. Creează utilizatorul
9. **SALVEAZA** URL-ul de login, username și parolă (le vei folosi)

### Pasul 1.2: Creează Access Keys pentru Acces Programatic

1. Mergi la **Users** → Click `metal-list-deployer`
2. Tab: **Security credentials**
3. Scroll jos → **Access keys** → **Create access key**
4. Use case: **Command Line Interface (CLI)**
5. Click **Create access key**
6. **COPIAZA și SALVEAZA** Access Key ID și Secret Access Key (nu-i împărți)

Vei folosi acestea pentru:
- AWS CLI (upload pe S3)
- EC2 deployment

---

## Partea 2: Configurare EC2

### Pasul 2.1: Creează Security Group (Reguli Firewall)

1. Mergi la **EC2** → Sidebar stâng → **Security Groups**
2. **Create security group**
   - Nume: `metal-list-sg`
   - Descriere: "Security group for Metal List"
   - VPC: (default)

3. Adaugă reguli inbound:
   ```
   Regula 1: HTTP
   - Type: HTTP (Port 80)
   - Source: Anywhere (0.0.0.0/0)
   
   Regula 2: HTTPS
   - Type: HTTPS (Port 443)
   - Source: Anywhere (0.0.0.0/0)
   
   Regula 3: SSH
   - Type: SSH (Port 22)
   - Source: My IP (auto-umplut sau IP-ul tău)
   ```

4. Click **Create security group**

### Pasul 2.2: Creează EC2 Instance

1. Mergi la **EC2** → **Instances** → **Launch instances**

2. **Pasul 1: Choose AMI**
   - Selectează: **Ubuntu Server 24.04 LTS** (free tier eligible)
   - Click **Select**

3. **Pasul 2: Choose instance type**
   - Type: **t2.micro** (FREE tier)
   - Click **Next**

4. **Pasul 3: Configure instance**
   - Number of instances: 1
   - Network: default VPC
   - Auto-assign public IP: ✅ Enable
   - Click **Next**

5. **Pasul 4: Add storage**
   - Size: 30 GB (default, suficient pentru SQLite + React build)
   - Click **Next**

6. **Pasul 5: Add tags**
   - Key: `Name`
   - Value: `metal-list`
   - Click **Next**

7. **Pasul 6: Configure security group**
   - Selectează: **metal-list-sg** (creat mai sus)
   - Click **Review and Launch**

8. **Pasul 7: Review**
   - Click **Launch**

9. **Selectează key pair**
   - Creează nou key pair (sau foloseți existentul)
   - Nume: `metal-list-key`
   - Type: RSA
   - Click **Create key pair**
   - **DESCARCA fișierul .pem** (îl vei folosi pentru SSH)
   - Click **Launch instances**

10. Asteaptă 1-2 minute pentru ca instanța să se pornească
    - Status: "running" ✅

---

## Partea 3: Conectare la EC2 & Deployment Cod

### Pasul 3.1: SSH în EC2

**Pe calculatorul local:**

```bash
# Navighează unde ai descărcat metal-list-key.pem
cd ~/Downloads  # sau unde ai salvat fișierul

# Fă cheia citibilă doar de tine
chmod 400 metal-list-key.pem

# Găsește IP-ul public al EC2
# Mergi la EC2 Console → Instances → Click pe instanța
# Copiază "Public IPv4 address" (ex: 54.123.45.67)

# SSH în instanță
ssh -i metal-list-key.pem ubuntu@54.123.45.67
# (înlocuiește 54.123.45.67 cu IP-ul tău real)
```

**Ar trebui acum să fii în instanța EC2 (terminal Ubuntu).**

### Pasul 3.2: Instalează Dependențe

```bash
# Actualizează sistemul
sudo apt update && sudo apt upgrade -y

# Instalează Python, pip, Node.js
sudo apt install -y python3.12 python3.12-venv python3-pip nodejs npm git

# Verifică instalări
python3 --version
node --version
npm --version
```

### Pasul 3.3: Clone Repository

```bash
# Clone din GitHub
git clone https://github.com/orvalus/Metal-List-project.git
cd Metal-List-project
```

### Pasul 3.4: Setup Backend

```bash
cd backend

# Creează virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalează dependențe
pip install -r requirements.txt

# Testează rulare
uvicorn main:app --reload --port 8000 &
# (rulează în background)

# Asteaptă 2 secunde, apoi testează
curl http://localhost:8000/docs
# Ar trebui să returneze HTML (FastAPI docs page)

# Oprește-l
pkill -f uvicorn
```

### Pasul 3.5: Setup Frontend

```bash
cd ../frontend

# Instalează dependențe
npm install

# Build pentru producție
npm run build

# Rezultat: frontend/dist/ folder cu fișiere statice
```

---

## Partea 4: Configurare S3 (Backup)

### Pasul 4.1: Creează S3 Bucket

1. Mergi la **S3** → **Create bucket**
2. Nume: `metal-list-backup-NUMELETAU` (trebuie să fie unic global)
   - Exemplu: `metal-list-backup-cornel-2026`
3. Regiune: aceeași ca EC2 (de obicei us-east-1)
4. **Debifează** "Block all public access" (îl vei accesa din EC2)
5. Click **Create bucket**

### Pasul 4.2: Creează IAM Policy pentru Acces S3

1. Mergi la **IAM** → **Policies** → **Create policy**
2. Service: **S3**
3. Actions: Bifează `GetObject`, `PutObject`, `ListBucket`
4. Resources: ARN-ul bucket-ului tău (ex: `arn:aws:s3:::metal-list-backup-cornel-2026`)
5. Click **Create policy**
6. Numește-o: `metal-list-s3-policy`

### Pasul 4.3: Atașează Policy la Deployer User

1. Mergi la **Users** → `metal-list-deployer`
2. **Add permissions** → **Attach policy**
3. Selectează `metal-list-s3-policy`
4. Click **Add permissions**

---

## Partea 5: Deploy pe EC2 (Producție)

### Pasul 5.1: Creează Script de Deployment

Pe EC2 instance, creează `~/deploy.sh`:

```bash
#!/bin/bash

cd ~/Metal-List-project

# Pull ultimul cod
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Omoară procesul vechi
pkill -f "uvicorn main:app" || true

# Pornește FastAPI în background
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# Frontend
cd ../frontend
npm install
npm run build

# Copiază frontend build în director web server
sudo mkdir -p /var/www/metal-list
sudo cp -r dist/* /var/www/metal-list/

# Pornește Nginx să servească frontend
sudo systemctl restart nginx

echo "Deployment completat!"
```

Fă-l executabil:
```bash
chmod +x ~/deploy.sh
```

### Pasul 5.2: Instalează Nginx (Reverse Proxy)

```bash
sudo apt install -y nginx

# Creează config Nginx
sudo tee /etc/nginx/sites-available/metal-list > /dev/null << 'EOFNGINX'
server {
    listen 80 default_server;
    server_name _;

    # Frontend (React)
    location / {
        root /var/www/metal-list;
        try_files $uri /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOFNGINX

# Activeaza site-ul
sudo ln -s /etc/nginx/sites-available/metal-list /etc/nginx/sites-enabled/

# Elimină site-ul default
sudo rm /etc/nginx/sites-enabled/default

# Testează config
sudo nginx -t

# Pornește Nginx
sudo systemctl restart nginx
```

### Pasul 5.3: Rulează Deployment

```bash
./deploy.sh
```

---

## Partea 6: Verifică Deployment

### Verifică dacă serviciile rulează

```bash
# Backend
curl http://localhost:8000/docs
# Ar trebui să returneze FastAPI docs

# Frontend
curl http://localhost/
# Ar trebui să returneze React HTML

# Verifică IP-ul public
curl http://169.254.169.254/latest/meta-data/public-ipv4
# Copiază acest IP
```

### Vizitează app-ul

Deschide browserul și mergi la:
```
http://IP_TU_EC2_PUBLIC
```

Ar trebui să vezi Metal List app-ul! 🎉

---

## Partea 7: Configurare S3 Backup

### Creează script de backup pe EC2

```bash
# Instalează AWS CLI
pip install awscli

# Configurează AWS credentials
aws configure
# Introdu:
# - Access Key ID: (din Pasul 1.2)
# - Secret Access Key: (din Pasul 1.2)
# - Default region: us-east-1
# - Default output: json
```

### Script de backup

Creează `~/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/home/ubuntu/Metal-List-project/backend"
S3_BUCKET="metal-list-backup-NUMELETAU"  # Schimbă asta!
DB_FILE="$BACKUP_DIR/metal_list.db"

# Oprește FastAPI pe scurt
pkill -f "uvicorn main:app" || true

# Asteaptă shutdown curat
sleep 2

# Backup în S3
aws s3 cp $DB_FILE s3://$S3_BUCKET/metal_list_$(date +%Y%m%d_%H%M%S).db

# Pornește FastAPI din nou
cd $BACKUP_DIR
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

echo "Backup completat!"
```

Fă-l executabil:
```bash
chmod +x ~/backup.sh
```

### Programează backup-uri zilnice (cron)

```bash
crontab -e
# Adaugă această linie (rulează zilnic la 2 AM):
0 2 * * * /home/ubuntu/backup.sh

# Salveaza și ieși
```

---

## Partea 8: Domeniu Personalizat (Opțional)

Dacă vrei `metal-list.com` în loc de IP EC2:

1. Cumpără domeniu din **Route 53** sau extern (Namecheap, GoDaddy)
2. Mergi la **Route 53** → **Hosted zones** → **Create hosted zone**
3. Domeniu: `metal-list.com`
4. Copiază **Name servers**
5. Mergi la registrarul tău de domeniu și actualizează nameserver-urile
6. Înapoi în Route 53 → **Create record**
   - Type: **A**
   - Value: IP-ul public al EC2
   - Click **Create**
7. Asteaptă 24 de ore pentru propagare DNS
8. Vizitează `http://metal-list.com` 🎉

---

## Partea 9: Monitor & Mentenanță

### Verifică log-uri

```bash
# Backend
tail -f ~/Metal-List-project/backend/backend.log

# Nginx
sudo tail -f /var/log/nginx/access.log
```

### Backup manual oricând

```bash
./backup.sh
```

### Redeploy schimbări cod

```bash
./deploy.sh
```

### SSH înapoi oricând

```bash
ssh -i metal-list-key.pem ubuntu@IP_TU_EC2
```

---

## Rezolvare Probleme

### Instance nu se pornește
- Verifică security group permite SSH (port 22)
- Verifică key pair se potrivește

### Backend nu se pornește
```bash
cd ~/Metal-List-project/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
# Caută erori
```

### Nu poți accesa frontend
```bash
sudo systemctl status nginx
sudo systemctl restart nginx
```

### S3 backup eșuează
```bash
aws s3 ls  # Verifică credențiale
aws configure  # Reconfigurează
```

---

## Rezumat Cost

| Serviciu | Free Tier | Cost Lunar |
|----------|-----------|------------|
| EC2 t2.micro | 750 ore/lună | $0 |
| S3 stocare | 5GB/lună | $0 |
| S3 transfer date | 20k GET, 2k PUT | $0 |
| Domeniu (Route 53) | N/A | $0.50 |
| **Total** | | **$0.50/lună** |

**Forever gratuit dacă rămâi în limitele free tier!**

---

## Pași Următori

1. ✅ Verifică că totul funcționează
2. ✅ Configurează backup-uri (cron job)
3. ✅ Adaugă domeniu personalizat (opțional)
4. ✅ Partajează cu prietenii
5. ✅ Monitor log-uri ocazional

Gata! 🚀
