# AWS Core Services - Learning Notes

---

## Table of Contents
1. [EC2 (Elastic Compute Cloud)](#ec2-elastic-compute-cloud)
2. [IAM (Identity & Access Management)](#iam-identity--access-management)
3. [Security Groups](#security-groups)
4. [VPC (Virtual Private Cloud)](#vpc-virtual-private-cloud)
5. [VPN (Virtual Private Network)](#vpn-virtual-private-network)
6. [S3 (Simple Storage Service)](#s3-simple-storage-service)
7. [Elastic Load Balancer (ELB)](#elastic-load-balancer-elb)
8. [Auto Scaling](#auto-scaling)
9. [Route 53](#route-53)
10. [CloudWatch](#cloudwatch)

---

## EC2 (Elastic Compute Cloud)

### What is EC2?
EC2 is a virtual server (machine) in the cloud. Instead of buying physical hardware, you rent a computer from AWS and pay only for what you use.

### Key Concepts

| Term | Meaning |
|------|---------|
| Instance | A running virtual server |
| AMI (Amazon Machine Image) | Template/snapshot to launch an instance (OS + software) |
| Instance Type | Hardware config (CPU, RAM, storage) e.g., t2.micro, m5.large |
| Key Pair | SSH keys to securely connect to your instance |
| EBS (Elastic Block Store) | Virtual hard disk attached to EC2 |
| Elastic IP | A static public IP that doesn't change on restart |
| User Data | Bootstrap script that runs on first launch |

### Instance Types

| Family | Purpose | Example Use Case |
|--------|---------|-----------------|
| t2/t3 | General purpose (burstable) | Web servers, dev environments |
| m5 | General purpose (balanced) | Application servers |
| c5 | Compute optimized | Batch processing, ML inference |
| r5 | Memory optimized | In-memory databases, caching |
| p3/p4 | GPU instances | ML training, video rendering |

### Pricing Models

| Model | Description | Discount |
|-------|-------------|----------|
| On-Demand | Pay per hour/second, no commitment | None |
| Reserved | 1 or 3 year commitment | Up to 72% |
| Spot | Bid on unused capacity (can be interrupted) | Up to 90% |
| Savings Plan | Flexible commitment-based | Up to 72% |

### Common EC2 Commands
```bash
# Launch instance (via CLI)
aws ec2 run-instances --image-id ami-xxxxx --instance-type t2.micro --key-name mykey

# List instances
aws ec2 describe-instances

# Start/Stop/Terminate
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# SSH into instance
ssh -i "mykey.pem" ec2-user@<public-ip>
```

### EC2 Instance Lifecycle
```
Pending → Running → Stopping → Stopped → Terminated
                  ↘ Shutting Down → Terminated
```

---

## IAM (Identity & Access Management)

### What is IAM?
IAM controls WHO can access WHAT in your AWS account. It's the security gatekeeper.

### Core Components

| Component | What it is | Example |
|-----------|-----------|---------|
| User | A person or application | "rahul", "deploy-bot" |
| Group | Collection of users | "Developers", "Admins" |
| Role | Temporary permissions for services/users | EC2 accessing S3 |
| Policy | JSON document defining permissions | Allow read-only S3 access |

### IAM Role vs User

| | User | Role |
|--|------|------|
| For | People, long-term access | Services, temporary access |
| Credentials | Password + Access Keys | Temporary security tokens |
| Example | Developer logging into console | EC2 instance reading from S3 |

### Policy Example (Allow S3 Read-Only)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

### Policy Example (Full Admin Access)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

### IAM Best Practices
- Never use root account for daily tasks
- Enable MFA (Multi-Factor Authentication) on all accounts
- Follow **least privilege** — give minimum permissions needed
- Use Roles for services (not access keys)
- Rotate credentials regularly
- Use IAM Access Analyzer to audit permissions

### Common IAM Commands
```bash
# List users
aws iam list-users

# Create user
aws iam create-user --user-name newuser

# Attach policy to user
aws iam attach-user-policy --user-name newuser --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create role
aws iam create-role --role-name MyRole --assume-role-policy-document file://trust-policy.json
```

---

## Security Groups

### What is a Security Group?
A Security Group is a **virtual firewall** for your EC2 instance. It controls inbound (incoming) and outbound (outgoing) traffic.

### Key Points
- Security Groups are **stateful** — if you allow inbound traffic, the response is automatically allowed out
- Default: All inbound DENIED, all outbound ALLOWED
- You can only add ALLOW rules (no explicit DENY)
- Attached at the instance level
- Multiple instances can share the same security group
- An instance can have multiple security groups

### Common Rules

| Type | Protocol | Port | Source | Use Case |
|------|----------|------|--------|----------|
| SSH | TCP | 22 | Your IP | Remote access to Linux |
| HTTP | TCP | 80 | 0.0.0.0/0 | Web traffic |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Secure web traffic |
| Custom TCP | TCP | 3000 | 0.0.0.0/0 | Node.js app |
| Custom TCP | TCP | 5000 | 0.0.0.0/0 | Flask app |
| MySQL | TCP | 3306 | sg-xxxxx | Database (from app SG only) |
| PostgreSQL | TCP | 5432 | 10.0.0.0/16 | Database (from VPC only) |

### Security Group vs NACL (Network ACL)

| | Security Group | NACL |
|--|---------------|------|
| Level | Instance level | Subnet level |
| Stateful? | Yes | No (must define both directions) |
| Rules | Allow only | Allow and Deny |
| Evaluation | All rules evaluated together | Rules evaluated in order |

### Best Practices
- Never open port 22 (SSH) to 0.0.0.0/0 — restrict to your IP
- Use separate security groups for web, app, and database tiers
- Reference other security groups instead of IP ranges where possible
- Regularly audit unused or overly permissive rules

---

## VPC (Virtual Private Cloud)

### What is VPC?
A VPC is your own **isolated private network** inside AWS. Think of it as your own data center in the cloud where you control the networking.

### Key Components

| Component | What it does |
|-----------|-------------|
| VPC | Your isolated network (e.g., 10.0.0.0/16) |
| Subnet | A segment of VPC (public or private) |
| Internet Gateway (IGW) | Connects VPC to the internet |
| NAT Gateway | Lets private subnets access internet (outbound only) |
| Route Table | Rules that determine where traffic goes |
| NACL | Stateless firewall at subnet level |
| Elastic IP | Static public IP address |

### VPC Architecture
```
VPC (10.0.0.0/16)
│
├── Public Subnet (10.0.1.0/24) ──── Internet Gateway ──── Internet
│   ├── Web Server (EC2)
│   ├── Load Balancer
│   └── NAT Gateway
│
├── Private Subnet (10.0.2.0/24) ──── NAT Gateway (outbound only)
│   └── Application Server (EC2)
│
└── Private Subnet (10.0.3.0/24) ──── No internet access
    └── Database (RDS)
```

### Public vs Private Subnet

| | Public Subnet | Private Subnet |
|--|--------------|----------------|
| Internet access | Direct (via IGW) | Outbound only (via NAT) or none |
| Has public IP? | Yes | No |
| Use case | Web servers, load balancers | App servers, databases |
| Route table | Routes to IGW | Routes to NAT or local only |

### CIDR Notation Quick Reference
| CIDR | IPs Available | Use |
|------|--------------|-----|
| /16 | 65,536 | VPC |
| /24 | 256 | Subnet |
| /28 | 16 | Small subnet |
| /32 | 1 | Single IP |

### Default VPC vs Custom VPC
- AWS gives you a default VPC in each region (all subnets are public)
- For production, always create a custom VPC with proper public/private separation

---

## VPN (Virtual Private Network)

### What is AWS VPN?
AWS VPN creates a **secure encrypted tunnel** between your on-premises network (office/data center) and your AWS VPC over the public internet.

### Types of VPN

| Type | Use Case |
|------|----------|
| Site-to-Site VPN | Connect your office network to AWS VPC |
| Client VPN | Individual users connect to AWS (like remote work) |

### Site-to-Site VPN Components

| Component | Where | What it does |
|-----------|-------|-------------|
| Virtual Private Gateway (VGW) | AWS side | VPN endpoint on AWS |
| Customer Gateway (CGW) | Your side | Your router/firewall device |
| VPN Tunnel | Between | Encrypted IPsec connection |

### Architecture
```
Your Office Network ──── Customer Gateway ════ VPN Tunnel ════ Virtual Private Gateway ──── VPC
   (10.1.0.0/16)          (your router)      (encrypted)         (AWS side)            (10.0.0.0/16)
```

### VPN vs Direct Connect

| | VPN | Direct Connect |
|--|-----|---------------|
| Connection | Over public internet | Dedicated physical line |
| Setup time | Minutes | Weeks/months |
| Cost | Low | High |
| Bandwidth | Up to 1.25 Gbps | Up to 100 Gbps |
| Encryption | Built-in (IPsec) | Not by default |
| Use case | Quick setup, backup | High bandwidth, consistent latency |

---

## S3 (Simple Storage Service)

### What is S3?
S3 is **object storage** — unlimited storage for files, images, backups, logs, etc. Files are stored in "buckets."

### Key Concepts

| Term | Meaning |
|------|---------|
| Bucket | Container for objects (globally unique name) |
| Object | A file + metadata (up to 5TB) |
| Key | The full path/name of the object |
| Versioning | Keep multiple versions of the same file |
| Storage Class | Different tiers based on access frequency |

### Storage Classes

| Class | Access | Cost | Use Case |
|-------|--------|------|----------|
| Standard | Frequent | $$$ | Active data, websites |
| Intelligent-Tiering | Auto-moves | $$ | Unknown patterns |
| Standard-IA | Infrequent | $$ | Backups accessed monthly |
| Glacier Instant | Archive | $ | Rarely accessed, instant retrieval |
| Glacier Deep Archive | Archive | ¢ | Compliance data, 12hr retrieval |

### Common S3 Commands
```bash
# List buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-unique-bucket-name

# Upload file
aws s3 cp myfile.txt s3://my-bucket/

# Download file
aws s3 cp s3://my-bucket/myfile.txt ./

# Sync folder
aws s3 sync ./local-folder s3://my-bucket/folder

# Delete file
aws s3 rm s3://my-bucket/myfile.txt
```

### S3 Bucket Policy Example (Public Read)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

---

## Elastic Load Balancer (ELB)

### What is ELB?
A Load Balancer distributes incoming traffic across multiple EC2 instances so no single server gets overwhelmed.

### Types

| Type | Layer | Use Case |
|------|-------|----------|
| ALB (Application) | Layer 7 (HTTP/HTTPS) | Web apps, path-based routing |
| NLB (Network) | Layer 4 (TCP/UDP) | Gaming, IoT, ultra-low latency |
| GLB (Gateway) | Layer 3 | Third-party firewalls/appliances |

### How ALB Works
```
Users ──→ ALB ──→ Target Group ──→ EC2 Instance 1
                              ──→ EC2 Instance 2
                              ──→ EC2 Instance 3
```

### Key Features
- Health checks — automatically stops sending traffic to unhealthy instances
- SSL termination — handles HTTPS at the load balancer level
- Sticky sessions — route same user to same instance
- Path-based routing — /api → backend servers, /images → media servers

---

## Auto Scaling

### What is Auto Scaling?
Automatically adds or removes EC2 instances based on demand. Scale out when traffic is high, scale in when it's low.

### Components

| Component | What it does |
|-----------|-------------|
| Launch Template | Blueprint for new instances (AMI, type, SG, etc.) |
| Auto Scaling Group (ASG) | Manages the fleet of instances |
| Scaling Policy | Rules for when to scale |

### Scaling Policies

| Type | How it works |
|------|-------------|
| Target Tracking | Keep CPU at 50% — adds/removes instances to maintain |
| Step Scaling | If CPU > 70% add 2, if CPU > 90% add 4 |
| Scheduled | Scale up at 9 AM, scale down at 6 PM |

### Architecture with ELB + Auto Scaling
```
Users ──→ ALB ──→ Auto Scaling Group
                    ├── EC2 (AZ-a)
                    ├── EC2 (AZ-b)
                    └── EC2 (AZ-c)  ← added/removed automatically
```

---

## Route 53

### What is Route 53?
AWS DNS service — translates domain names (myapp.com) to IP addresses. Also handles domain registration and health checks.

### Routing Policies

| Policy | Use Case |
|--------|----------|
| Simple | One record, one destination |
| Weighted | Split traffic (80% to v1, 20% to v2) |
| Latency | Route to lowest-latency region |
| Failover | Primary/secondary (disaster recovery) |
| Geolocation | Route based on user's country |

---

## CloudWatch

### What is CloudWatch?
Monitoring and observability service. Collects metrics, logs, and triggers alarms.

### Key Features

| Feature | What it does |
|---------|-------------|
| Metrics | CPU, memory, disk, network stats |
| Alarms | Alert when threshold is breached (e.g., CPU > 80%) |
| Logs | Centralized log collection from EC2, Lambda, etc. |
| Dashboards | Visual graphs of your metrics |
| Events | React to state changes (instance stopped, etc.) |

### Common Metrics to Monitor
- EC2: CPUUtilization, NetworkIn/Out, DiskReadOps
- RDS: DatabaseConnections, FreeStorageSpace
- ALB: RequestCount, TargetResponseTime, HTTP 5xx errors

---

## Quick Reference - How Services Connect

```
Internet
   │
   ▼
Route 53 (DNS) ──→ CloudFront (CDN)
   │
   ▼
VPC
├── Public Subnet
│   ├── ALB (Load Balancer)
│   └── NAT Gateway
├── Private Subnet
│   ├── EC2 (Auto Scaling Group)
│   └── EC2 has IAM Role → accesses S3
└── Private Subnet
    └── RDS Database

Security Groups protect each resource
CloudWatch monitors everything
VPN connects your office to the VPC
```

---

## Useful AWS CLI Setup
```bash
# Install AWS CLI
# Mac
brew install awscli

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Key, Region (ap-south-1), Output format (json)

# Verify
aws sts get-caller-identity
```

---


## how can we we connect to sc2 if ssh key pair we dont have ssm manager is down and we dont have usernasme and password
## without havuing key pair how can we connect to ssh