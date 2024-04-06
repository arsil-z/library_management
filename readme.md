# Assignment Part 1

To setup run:
```commandline
docker compose up --build
```

To setup all the tables after the server starts:
Hit this endpoint: http://0.0.0.0:10000/health_check_db

API Endpoint(s) for handling book checkouts and returns:
```curl
curl --location 'http://0.0.0.0:10000/api/library/circulation' \
--header 'Content-Type: application/json' \
--data '[
    {
        "eventtype": "checkout",
        "book_id": 1000,
        "member_id": 2003,
        "date": "2023-05-10"
    },
    {
        "eventtype": "checkout",
        "book_id": 1000,
        "member_id": 2013,
        "date": "2023-05-11"
    },
    {
        "eventtype": "checkout",
        "book_id": 1000,
        "member_id": 2000,
        "date": "2023-05-18"
    },
    {
        "eventtype": "return",
        "book_id": 1000,
        "member_id": 2013,
        "date": "2023-05-22"
    },
    {
        "eventtype": "checkout",
        "book_id": 1002,
        "member_id": 2006,
        "date": "2023-05-02"
    },
    {
        "eventtype": "return",
        "book_id": 1002,
        "member_id": 2006,
        "date": "2023-05-08"
    },
    {
        "eventtype": "return",
        "book_id": 1002,
        "member_id": 2018,
        "date": "2023-05-18"
    },
    {
        "eventtype": "checkout",
        "book_id": 1011,
        "member_id": 2019,
        "date": "2023-05-08"
    }
]'
```


# Assignment Part 2
The file named `max_sum_subarray.py` has the solution to the given problem
To run it, just do `python3 max_sum_subarray.py`