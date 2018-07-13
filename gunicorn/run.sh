#!/usr/bin/env bash
gunicorn --workers=2 app:app
