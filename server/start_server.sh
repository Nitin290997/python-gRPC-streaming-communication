echo "Starting Network Server"
python3 /root/server/gRPC_server.py \
  --serverHost 0.0.0.0 \
  --serverSecurePort 9010 \
  --serverPort 8010 \
  --logLevel DEBUG
