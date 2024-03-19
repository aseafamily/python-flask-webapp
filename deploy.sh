#!/bin/bash

# Copy all files except test.db to the deployment directory
rsync -av --exclude='test.db' ./ $DEPLOYMENT_TARGET
