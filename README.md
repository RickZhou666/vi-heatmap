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


# Tips

1. there should not be any empty line between html, otherwise it's will be malformed
```html
GOOD
<div style='background-color:#17456f; color:white; writing-mode: sideways-lr; text-align:right; padding:10px;'>
                Thumbnails Click:<br>""" + data['Thumbnails Click'] + """</div>
<div style='background-color:#1f3b73; color:white; padding:6px;'>
    Image Thumbnails Arrow Click:<br>""" + data['Image Thumbnails Arrow Click'] + """</div>

BAD
<div style='background-color:#17456f; color:white; writing-mode: sideways-lr; text-align:right; padding:10px;'>
                Thumbnails Click:<br>""" + data['Thumbnails Click'] + """</div>

<div style='background-color:#1f3b73; color:white; padding:6px;'>
    Image Thumbnails Arrow Click:<br>""" + data['Image Thumbnails Arrow Click'] + """</div>
```


2. padding
```bash
In CSS, the "padding" property can be set in several ways:
        - padding-top
        - padding-right
        - padding-bottom
        - padding-left
        - padding (shorthand for all four sides)
```