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

## Streamlit Tips
1. why set first_run set the key as true?
```python
# 第一次：tab_key 不在 session_state，代表是首次进入该 tab
# 执行 query 是你想要的默认行为
# 设置为 False 后，下次再 rerun 时会跳过这段逻辑
first_run = "dweb_heatmap_first_run"
if first_run not in st.session_state:
    st.session_state[first_run] = True
    st.session_state["data_loaded"] = False
    run_query_and_update_state(filters, "dweb_heatmap_first_run - Graph rendering in progress...")
    st.session_state[first_run] = False


```

每次你和页面交互（如选 filter、切换 tab、拖动 slider）都会触发一次 脚本 rerun。所以你必须通过 st.session_state 显式控制「哪些逻辑只能跑一次」。




<br><br><br>

## HTML/CSS Tips
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

<br><br><br>

## VSC tips
1. how to regexp search for starting empty lines
```bash
^\s*$
```