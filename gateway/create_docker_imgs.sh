for i in gwi gwf-1 gwf-2 gwf-3
do
    echo $i
    sudo docker build --network host --build-arg GW_ID=$i -t theofontana/gateway:$i .
done