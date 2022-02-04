#!/bin/bash
mkdir private
pushd private

echo "12345" > admin
echo "12345:abcde" > token
echo "{}" > users

popd
echo "File creation complete. But please put token and admin ID manually!"