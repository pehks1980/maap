#!/bin/sh
ls -l;
export $(cat .env.dev| grep -v "#");
