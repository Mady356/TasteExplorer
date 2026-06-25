#!/bin/bash

# TasteExplorer Spotify Setup Script

echo "═══════════════════════════════════════════════════════"
echo "  TasteExplorer - Spotify API Setup"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✓ Found .env file"

    # Check if Spotify credentials are set
    if grep -q "your_spotify_client_id_here" .env; then
        echo "✗ Spotify credentials not configured"
        echo ""
        echo "Please follow these steps:"
        echo ""
        echo "1. Go to: https://developer.spotify.com/dashboard"
        echo "2. Log in with your Spotify account"
        echo "3. Click 'Create app'"
        echo "4. Fill in:"
        echo "   - App name: TasteExplorer"
        echo "   - App description: Music discovery platform"
        echo "   - Redirect URI: http://localhost:8000/auth/spotify/callback"
        echo "   - Check 'Web API'"
        echo "5. Click 'Save'"
        echo "6. Copy your Client ID and Client Secret"
        echo "7. Edit .env file and replace:"
        echo "   SPOTIFY_CLIENT_ID=your_spotify_client_id_here"
        echo "   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here"
        echo ""
        echo "Then run: docker-compose restart api"
        echo ""
        exit 1
    else
        echo "✓ Spotify credentials configured"

        # Extract credentials (first 10 chars)
        CLIENT_ID=$(grep "SPOTIFY_CLIENT_ID=" .env | cut -d'=' -f2 | cut -c1-10)
        echo "  Client ID: ${CLIENT_ID}..."
        echo ""
        echo "✓ Setup complete!"
        echo ""
        echo "Next steps:"
        echo "1. Start services: docker-compose up -d"
        echo "2. Open: http://localhost:3000"
        echo "3. Click 'Connect Spotify'"
        echo ""
    fi
else
    echo "✗ .env file not found"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "Now configure Spotify credentials (see above steps)"
fi
