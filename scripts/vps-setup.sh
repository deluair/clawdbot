#!/bin/bash
# ============================================================
# OpenClaw VPS Setup Script — OVHcloud Ubuntu 25.04
# Run this on your VPS after SSH'ing in
# ============================================================
set -euo pipefail

echo "🦞 OpenClaw VPS Setup — Starting..."

# 1. System updates
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install Node.js 22 LTS
echo "📦 Installing Node.js 22..."
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt install -y nodejs

# 3. Install pnpm
echo "📦 Installing pnpm..."
npm install -g pnpm

# 4. Install Docker (for sandbox mode, optional)
echo "🐳 Installing Docker..."
sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# 5. Clone OpenClaw
echo "🦞 Cloning OpenClaw..."
cd ~
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 6. Install deps and build
echo "🔧 Installing dependencies..."
pnpm install
pnpm ui:build
pnpm build

# 7. Create config directory
mkdir -p ~/.openclaw

# 8. Create openclaw.json config
cat > ~/.openclaw/openclaw.json << 'JSONEOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3-flash-preview"
      }
    }
  },
  "gateway": {
    "bind": "lan",
    "auth": {
      "mode": "token"
    }
  }
}
JSONEOF

# 9. Create .env
GATEWAY_TOKEN=$(openssl rand -hex 32)
cat > ~/openclaw/.env << ENVEOF
# OpenClaw Environment
OPENCLAW_GATEWAY_TOKEN=${GATEWAY_TOKEN}
GEMINI_API_KEY=AIzaSyBcFlUcpdqdj68PveVWqTDui4Nz-bapM_g
ENVEOF

echo ""
echo "✅ OpenClaw installed and built!"
echo ""
echo "🔑 Your gateway token: ${GATEWAY_TOKEN}"
echo "   Save this! You'll need it to connect clients."
echo ""
echo "🚀 To start the gateway:"
echo "   cd ~/openclaw && node dist/index.js gateway --port 18789 --verbose"
echo ""
echo "💡 To install as a system service (auto-start on boot):"
echo "   cd ~/openclaw && pnpm openclaw onboard --install-daemon"
echo ""
echo "🦞 Done! EXFOLIATE! EXFOLIATE!"
