# Web Scraping Agent – Real Use Case Demonstrations
Generated on: 2025-12-03 19:36:55.680037
## Valid stock: META

### Input URL
https://finance.yahoo.com/quote/META

### Researcher Output
```
{"stock_price": 6847.84, "source": "https://finance.yahoo.com/quote/META"}
```

### Evaluator Output
```
{
    "evaluation": "SUCCESS",
    "reason": "JSON contains exactly 'stock_price' and 'source', valid numeric price.",
    "is_valid_price": true
}
```

## Valid stock: AAPL

### Input URL
https://finance.yahoo.com/quote/AAPL

### Researcher Output
```
{"stock_price": 278.12, "source": "https://finance.yahoo.com/quote/AAPL"}
```

### Evaluator Output
```
{
    "evaluation": "SUCCESS",
    "reason": "JSON contains valid price and source.",
    "is_valid_price": true
}
```

## Valid stock: GOOG

### Input URL
https://finance.yahoo.com/quote/GOOG

### Researcher Output
```
{"stock_price": 322.09, "source": "https://finance.yahoo.com/quote/GOOG"}
```

### Evaluator Output
```
{
    "evaluation": "SUCCESS",
    "reason": "JSON contains valid price and source.",
    "is_valid_price": true
}
```

## Invalid ticker

### Input URL
https://finance.yahoo.com/quote/INVALID

### Researcher Output
```
{"error": "Price not found"}
```

### Evaluator Output
```
{
    "evaluation": "FAILURE",
    "reason": "Missing stock_price and source due to invalid ticker.",
    "is_valid_price": false
}
```

## Non-stock homepage

### Input URL
https://finance.yahoo.com/

### Researcher Output
```
{"error": "Invalid URL. Not a stock quote page."}
```

### Evaluator Output
```
{
    "evaluation": "FAILURE",
    "reason": "URL is not a stock quote page.",
    "is_valid_price": false
}
```

