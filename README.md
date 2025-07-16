# vi-heatmap


1. connect to spark
2. get filter combinations and assemble sql
3. submit sql to spark and get results
4. streamlit reader by the results


```bash
# execute streamlit app
streamlit run app.py
```

<br><br><br>


# docker
```bash
$ docker build -t vi-heatmap-app .

$ docker run -p 8501:8501 vi-heatmap-app

```
