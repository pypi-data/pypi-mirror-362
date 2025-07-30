#!/bin/bash
echo "START Logstash testauto"
echo "Initialize logstash with input files"
echo "START Logstash on mock configuration"
/usr/share/logstash/bin/logstash --log.level=info  --path.settings /usr/share/logstash/config --config.reload.automatic
echo "END test"