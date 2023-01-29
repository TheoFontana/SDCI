curl -X POST -d '{
    "dpid": 2,
    "table_id":0,
    "priority":11111,
    "match":{
        "nw_src": "10.1.0.60",
        "nw_dst": "10.1.0.11",
        "dl_type": "2048",

    },
    "actions":[
        {
            "type": "SET_FIELD",
            "field": "ipv4_src",
            "value": "10.1.0.10"
        },
        {
            "type": "OUTPUT",
            "port": "NORMAL"
        }
    ]
 }' http://localhost:8080/stats/flowentry/add