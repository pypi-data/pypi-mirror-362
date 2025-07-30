# Memory Hub MCP Server - Docker Setup

A high-performance, locally-hosted Memory Hub for AI engineering agents, now containerized for easy deployment and development.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- LM Studio running on `localhost:1234` with:
  - Nomic embedding model (`text-embedding-nomic-embed-text-v1.5`)
  - Gemma-3-4b model for summarization

### One-Command Startup
```bash
# Make the script executable (first time only)
chmod +x scripts/start.sh

# Start the entire stack
./scripts/start.sh start
```

### Manual Docker Compose
```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📋 Services

| Service | Port | Description | Dashboard |
|---------|------|-------------|-----------|
| Memory Hub API | 8000 | FastAPI + MCP Server | http://localhost:8000/docs |
| Qdrant Vector DB | 6333 | Vector storage | http://localhost:6333/dashboard |
| LM Studio | 1234 | Embeddings & LLM | *External - must be running* |

## 🛠 Management Commands

The `scripts/start.sh` script provides convenient management:

```bash
./scripts/start.sh start     # Start all services
./scripts/start.sh stop      # Stop all services  
./scripts/start.sh restart   # Restart services
./scripts/start.sh rebuild   # Rebuild after code changes
./scripts/start.sh logs      # View live logs
./scripts/start.sh status    # Check health of all services
./scripts/start.sh clean     # Remove all data (destructive!)
./scripts/start.sh dev       # Start with hot reloading
```

## 🔧 Development Mode

For development with hot reloading:

```bash
# Start in development mode
./scripts/start.sh dev

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Development mode features:
- ✅ Hot reloading on code changes
- ✅ Read-write source mounting
- ✅ Debug environment variables
- ✅ No automatic restarts

## 🏗 Architecture

### Container Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Memory Hub    │────│     Qdrant      │    │   LM Studio     │
│   (FastAPI)     │    │  (Vector DB)    │    │  (Host System)  │
│   Port: 8000    │    │   Port: 6333    │    │   Port: 1234    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Volume Strategy
- **Qdrant Data**: Persistent named volume (`qdrant_storage`)
- **Source Code**: Mounted for development (read-only in production)
- **Assets**: Mounted for scope documents and logs

### Network Strategy
- **Internal**: Memory Hub ↔ Qdrant (Docker network)
- **External**: Memory Hub ↔ LM Studio (`host.docker.internal`)

## ⚙️ Configuration

### Environment Variables

The Docker setup supports these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `QDRANT_URL` | `http://qdrant:6333` | Qdrant connection (internal) |
| `LM_STUDIO_BASE_URL` | `http://host.docker.internal:1234/v1` | LM Studio connection |
| `ENABLE_QUANTIZATION` | `true` | Enable 75% memory reduction |
| `ENABLE_TENANT_OPTIMIZATION` | `true` | Multi-tenant storage optimization |
| `MIN_SCORE_THRESHOLD` | `0.60` | Minimum similarity score threshold |
| `ENABLE_GEMMA_SUMMARIZATION` | `true` | Enable/disable Gemma synthesis of search results |
| `HNSW_M` | `32` | HNSW connections per node |
| `HNSW_EF_CONSTRUCT` | `256` | HNSW construction quality |

### Production Optimizations Enabled
- ✅ **Scalar Quantization**: 75% memory reduction with INT8 compression
- ✅ **Multi-tenant Storage**: Optimized indexing for `app_id` and `project_id` fields
- ✅ **HNSW Tuning**: Enhanced parameters for production workloads
- ✅ **Field Indexing**: Optimized metadata filtering

## 🔍 Health Monitoring

### Health Check Endpoints
- Memory Hub: http://localhost:8000/health
- Qdrant: http://localhost:6333/health
- LM Studio: http://localhost:1234/v1/models

### Status Command
```bash
./scripts/start.sh status
```

Shows:
- Container status
- Health check results
- Service accessibility

## 📊 Performance Benefits

### Docker vs Native Deployment
| Benefit | Description |
|---------|-------------|
| **Isolation** | No conflicts with system dependencies |
| **Reproducibility** | Same environment every time |
| **Easy Scaling** | Ready for multi-instance deployment |
| **Clean Management** | Simple start/stop without process hunting |
| **Production Ready** | Professional deployment approach |

### Memory Optimizations
- **75% reduction** with scalar quantization
- **Multi-tenant efficiency** with optimized storage
- **Production HNSW** parameters for better accuracy

## 🐛 Troubleshooting

### Common Issues

**1. LM Studio Connection Fails**
```bash
# Check if LM Studio is running
curl http://localhost:1234/v1/models

# Check Docker logs
docker-compose logs memory-hub
```

**2. Qdrant Connection Issues**
```bash
# Check Qdrant health
curl http://localhost:6333/health

# Restart Qdrant service
docker-compose restart qdrant
```

**3. Memory Hub Won't Start**
```bash
# Check all logs
docker-compose logs

# Rebuild container
./scripts/start.sh rebuild
```

**4. Permission Issues (Development)**
```bash
# Set correct user ID in dev mode
export UID=$(id -u) GID=$(id -g)
./scripts/start.sh dev
```

### Data Recovery

**Reset Everything (Nuclear Option)**
```bash
./scripts/start.sh clean
./scripts/start.sh start
```

**Backup Qdrant Data**
```bash
# Backup
docker cp memory-hub-qdrant:/qdrant/storage ./qdrant_backup

# Restore  
docker cp ./qdrant_backup memory-hub-qdrant:/qdrant/storage
```

## 🚀 Commercial Deployment

This Docker setup is production-ready for commercial deployment:

### Scaling Options
1. **Single Server**: Current setup with optimizations
2. **Multi-Container**: Multiple Memory Hub instances behind load balancer
3. **Distributed**: Qdrant cluster with automatic sharding

### Security Features
- ✅ Non-root container user
- ✅ Multi-stage builds for minimal attack surface
- ✅ Health checks for automatic restart
- ✅ Volume isolation

### Next Steps for Production
- Add TLS/HTTPS termination
- Implement authentication/authorization
- Add monitoring (Prometheus/Grafana)
- Set up automated backups

## 📝 Development Notes

### Workflow
1. Make code changes
2. Either:
   - **Development mode**: Changes auto-reload
   - **Production mode**: Run `./scripts/start.sh rebuild`

### Debugging
```bash
# Access container shell
docker exec -it memory-hub-api bash

# View container environment
docker exec memory-hub-api env

# Check Python packages
docker exec memory-hub-api pip list
```

### Custom Configuration
Override any setting by setting environment variables in `docker-compose.override.yml` or `.env` file.

## 🌐 MCP Client Configuration

### **Cursor MCP Setup**

Add to your `~/.cursor/mcp_servers/mcp.json`:

#### **Local Development (recommended)**
```json
{
  "local-memory-hub": {
    "url": "http://localhost:8000/mcp",
    "disabled": false,
    "autoApprove": ["add_memory", "search_memories", "health"]
  }
}
```

#### **Remote Server Access**
```json
{
  "remote-memory-hub": {
    "url": "http://YOUR_SERVER_IP:8000/mcp",
    "disabled": false,
    "autoApprove": ["add_memory", "search_memories", "health"]
  }
}
```

### **Required Restart**
After updating `mcp.json`, restart Cursor for changes to take effect.

---

## 🚀 Deployment Strategies

### **Strategy 1: Local Development (Recommended)**
**Best for:** Individual developers, testing, development

```bash
# Each developer runs their own stack
./scripts/start.sh start
```

**Requirements:**
- Docker + Docker Compose
- LM Studio running locally on port 1234
- Nomic embedding model + Gemma-3-4b loaded

**MCP Config:** `http://localhost:8000/mcp`

### **Strategy 2: Shared Memory Hub + Local LM Studio**
**Best for:** Teams sharing memory but keeping LM Studio local

**Server (Matt's Mac Studio):**
```bash
# Expose Memory Hub publicly
./scripts/start.sh start

# Configure router/firewall to forward port 8000
# External access: http://YOUR_PUBLIC_IP:8000
```

**Clients:** Each person runs their own LM Studio locally

**MCP Config:** `http://MATT_PUBLIC_IP:8000/mcp`

### **Strategy 3: Fully Shared Service**
**Best for:** Teams sharing everything, centralized AI services

**Server Setup:**
```bash
# Update docker-compose.yml to expose LM Studio
services:
  memory-hub:
    environment:
      - LM_STUDIO_BASE_URL=http://YOUR_PUBLIC_IP:1234/v1

# Expose both ports 8000 (Memory Hub) and 1234 (LM Studio)
```

**Network Configuration:**
- Port 8000: Memory Hub MCP endpoint
- Port 1234: LM Studio API (if sharing)
- Port 6333: Qdrant dashboard (optional, for debugging)

**MCP Config:** `http://SHARED_SERVER_IP:8000/mcp`

---

## 🔒 Security Considerations for Public Deployment

### **Firewall Rules**
```bash
# Allow Memory Hub MCP
sudo ufw allow 8000/tcp

# Allow LM Studio API (if sharing)
sudo ufw allow 1234/tcp

# Optional: Qdrant dashboard (debugging only)
sudo ufw allow 6333/tcp
```

### **Network Security**
- **VPN Recommended**: Use VPN for team access instead of public exposure
- **API Key Authentication**: Consider adding authentication to LM Studio
- **Rate Limiting**: Implement rate limiting for public endpoints
- **HTTPS**: Use reverse proxy (nginx/traefik) for TLS termination

### **Production Hardening**
```bash
# Create production override
cp docker-compose.yml docker-compose.prod.yml

# Remove development mounts
# Add resource limits
# Configure logging
```

---

## 📊 Monitoring & Maintenance

### **Health Monitoring**
```bash
# Check all services
./scripts/start.sh status

# Monitor logs
./scripts/start.sh logs

# Health endpoints
curl http://localhost:8000/health
curl http://localhost:6333/collections
```

### **Backup Strategy**
```bash
# Backup Qdrant data
docker cp memory-hub-qdrant:/qdrant/storage ./backup-$(date +%Y%m%d)

# Scheduled backups (add to crontab)
0 2 * * * /path/to/memory-hub/scripts/backup.sh
```

### **Updates**
```bash
# Update containers
./scripts/start.sh stop
docker-compose pull
./scripts/start.sh start

# Update Memory Hub code
git pull
./scripts/start.sh rebuild
```

---

## 💡 Why Docker?

Moving from manual process management to Docker provides:

1. **Professional Development Experience**: No more `launchctl` or process hunting
2. **Commercial Viability**: Easy customer onboarding with "just run docker-compose up"
3. **Consistent Environment**: Eliminates "works on my machine" issues
4. **Scaling Foundation**: Ready for load balancing and multi-instance deployment
5. **Clean Resource Management**: Isolated networking, storage, and compute

This containerized approach positions the Memory Hub as a professional, deployable service suitable for offering to other developers. 