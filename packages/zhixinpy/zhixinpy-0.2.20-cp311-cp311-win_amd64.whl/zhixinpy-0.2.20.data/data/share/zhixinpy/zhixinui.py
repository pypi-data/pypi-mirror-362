import os, shutil
import sys
import json
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import asyncio
import subprocess
import datetime as dt

import xloil as xlo

try:
    from PIL import Image
except ImportError:
    xlo.log.info("无法载入PIL")
from xloil.pandas import PDFrame


################## 特殊宏或者函数 ########################################

from zhixinpy.utils import Settings, catch_and_log, RGB, date_str_to_dt
from zhixinpy.zhixinpy import *
from zhixinpy.licclient import (
    g_verify_result,
    get_version,
)


def _ribbon_func_map(func: str):
    # Just finds the function with the given name in this module
    xlo.log.debug(f"Calling xlOil Ribbon '{func}'...")
    return globals()[func]


@paused
@xlo.func(command=True)
@catch_and_log(return_type="msg")
def create_condition_format_b_column(ctrl):
    create_condition_format()


_settings = Settings(xlo.source_addin().settings_file)


def get_python_home():
    return _settings.get_env_var("PYTHONEXECUTABLE")


def get_python_path():
    return _settings.get_env_var("PYTHONPATH")


def get_load_modules():
    value = _settings.python["LoadModules"]
    return ",".join(value)


def get_user_search_path():
    value = _settings.get_env_var("XLOIL_PYTHON_PATH")
    xlo.log(f"Search Path: {value}")
    return "" if value == ";" else value


def get_license_file():
    license_file = ""
    try:
        license_file = _settings.get_env_var("LICENSEFILE")
    except:
        license_file = "出错，没有找到license文件"
    return license_file


def get_license_data():
    if g_verify_result["code"] == 0:
        if g_verify_result.get("trial_days"):
            ret = g_verify_result.get("msg")
        else:
            ret = f'永久授权给{g_verify_result.get("email")}'
    else:
        ret = g_verify_result.get("msg")
    return ret


async def press_open_log(ctrl):
    xlo.log.flush()
    os.startfile(xlo.log.path)


def OnAboutButtonClick(control):
    content = (
        "版本: " + get_version() + "\n"
        "授权信息: " + get_license_data() + "\n\n"
        # "Python版本: " + sys.version.split(" ")[0] + "\n"
        # "python.exe路径: " + get_python_home() + "\n"
        # "PYTHONPATH变量: " + get_python_path() + "\n"
        # "模块搜索路径：" + get_user_search_path() + "\n"
        # "已加载模块：" + get_load_modules() + "\n\n"
        "文档地址：" + "zhixin.readthedocs.io" + "\n"
        "联系邮箱：" + "zhixin_excel@163.com" + "\n"
    )
    MsgBox(content=content, title="关于知心")


def load_register_file(ctrl):
    filename = xlo.app().GetOpenFilename(
        "知心注册文件 (*.lic), *.lic",
        MultiSelect=False,
        Title="请选择注册文件zhixinpy.lic",
    )
    if isinstance(filename, bool):  # 说明用户取消了
        return

    shutil.copy(filename, os.path.join(os.environ["appdata"], "xlOil", "zhixinpy.lic"))
    MsgBox("注册文件已导入，请重启Excel。\n之后点击知心-知心配置-关于知心，查看注册信息")


def preLoad(ctrl):
    def basic_func():
        from zhixinpy import (
            func_calendar,
            func_converter,
            func_filter,
            func_rtd,
            func_series,
            func_stat,
            func_text,
        )

    def tools_func():
        from zhixinpy import func_tools, func_lookup

    def chart_func():
        from zhixinpy import func_chart

    print_status("正在载入知心基础函数...")
    xlo.excel_callback(basic_func)

    print_status("正在载入知心图表函数...")
    xlo.excel_callback(chart_func)

    print_status("正在载入知心工具函数...")
    xlo.excel_callback(tools_func)

    MsgBox("已预载入所有知心函数，请丝滑地使用需要的函数.")


from zhixinpy.ribbon import (
    show_config_dialog,
    load_config,
    show_registration_dialog,
    open_website,
)
from zhixinpy.ribbon_chart_unified import (
    show_qrcode_dialog,
    show_image_dialog,
    show_video_dialog,
    show_download_dialog,
    show_mail_dialog,
    show_llm_dialog,
    show_llmex_dialog,
    show_llmgen_dialog,
    show_llm_translate_dialog,
    show_llm_categorize_dialog,
    show_llm_extract_dialog,
    show_llm_rewrite_dialog,
    show_crawler_dialog,
    show_genpubkey_dialog,
    show_encrypt_dialog,
    show_decrypt_dialog,
    show_tts_dialog,
    show_notice_dialog,
    show_convert_media_dialog,
    show_idcard_dialog,
    show_bankcard_dialog,
)
from zhixinpy.ribbon_chart_unified import (
    show_wordcloud_dialog,
    show_sankey_financial_dialog,
    show_line_dialog,
    show_line3d_dialog,
    show_area_dialog,
    show_pie_dialog,
    show_bar_dialog,
    show_scatter_dialog,
    show_scatter3d_dialog,
    show_geo_dialog,
    show_geoline_dialog,
    show_map_dialog,
    show_network_dialog,
    show_pie_bar_dialog,
    show_rank_dialog,
    show_rank_wind_dialog,
    show_sunburst_dialog,
    show_heatmap_dialog,
    show_candlestick_dialog, ###############
    show_funnel_dialog,
    show_map_bar_dialog,
    show_bar3d_dialog,
    show_surface3d_dialog,
    show_treemap_dialog,
    show_sankey_dialog,
    show_kchart_dialog,
)

gallery_1_images = [
    {"file_name": "chart-line.png", "chart_name": "折线图"},
    {"file_name": "chart-line3d.png", "chart_name": "三维折线图"},
    {"file_name": "chart-area.png", "chart_name": "面积图"},
    {"file_name": "chart-bar.png", "chart_name": "柱状图"},
    # {"file_name": "chart-histogram.png", "chart_name": "直方图"},
    {"file_name": "chart-pie.png", "chart_name": "饼图"},
    {"file_name": "chart-funnel.png", "chart_name": "漏斗图"},
    # {"file_name": "chart-violin.png", "chart_name": "小提琴图"},
    # {"file_name": "chart-ecdf.png", "chart_name": "累积分布函数图"},
    # {"file_name": "chart-strip.png", "chart_name": "条带图"},
]
gallery_2_images = [
    {"file_name": "chart-scatter.png", "chart_name": "散点图"},
    {"file_name": "chart-scatter3d.png", "chart_name": "三维散点图"},
    {"file_name": "chart-sankey.png", "chart_name": "桑基图"},
    {"file_name": "chart-sankey-financial.png", "chart_name": "桑基图(财报)"},
    {"file_name": "chart-treemap.png", "chart_name": "矩形树图"},
    {"file_name": "chart-sunburst.png", "chart_name": "旭日图"},
    {"file_name": "chart-network.png", "chart_name": "网络图"},
]
gallery_3_images = [
    {"file_name": "chart-map.png", "chart_name": "地图"},
    # {"file_name": "chart-map-scatter.png", "chart_name": "地图散点图"},
    # {"file_name": "chart-map-line.png", "chart_name": "地图路径图"},
    {"file_name": "chart-geo.png", "chart_name": "坐标图"},
    {"file_name": "chart-geo-line.png", "chart_name": "坐标路线图"},
    {"file_name": "chart-map-bar.png", "chart_name": "地图柱状图"},
]
gallery_4_images = [
    {"file_name": "chart-surface3d.png", "chart_name": "3D曲面图"},
    {"file_name": "chart-pie-bar.png", "chart_name": "饼状柱状图"},
    {"file_name": "chart-bar-3d.png", "chart_name": "3D柱状图"},
    {"file_name": "chart-rank.png", "chart_name": "排名图"},
    {"file_name": "chart-rank-wind.png", "chart_name": "排名图(Wind)"},
    {"file_name": "chart-wordcount.png", "chart_name": "词云图"},
    {"file_name": "chart-heatmap.png", "chart_name": "日历热力图"},
    {"file_name": "chart-kchart.png", "chart_name": "K线图"},
]


def get_gallery_1_count(ctrl):
    return len(gallery_1_images)


def get_gallery_1_label(ctrl, index: int):
    return gallery_1_images[index]["chart_name"]


def get_gallery_1_image(ctrl, index: int):
    image_path = (
        Path(os.path.join(sys.prefix, "share", "zhixinpy"))
        / gallery_1_images[index]["file_name"]
    )
    if not image_path.exists():
        return Image.new("RGB", (1, 1), (0, 0, 0))
    img  = Image.open(image_path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")  # 转换为 RGB 模式
    return img


def on_gallery_1_action(ctrl, galleryid: str, index: int):
    chart_name = gallery_1_images[index]["chart_name"]
    if chart_name == "折线图":
        show_line_dialog(ctrl)
    elif chart_name == "三维折线图":
        show_line3d_dialog(ctrl)
    elif chart_name == "面积图":
        show_area_dialog(ctrl)
    elif chart_name == "柱状图":
        show_bar_dialog(ctrl)
    elif chart_name == "直方图":
        display_formula(ctrl)
    elif chart_name == "饼图":
        show_pie_dialog(ctrl)
    elif chart_name == "漏斗图":
        show_funnel_dialog(ctrl)
    elif chart_name == "小提琴图":
        display_formula(ctrl)
    elif chart_name == "累积分布函数图":
        display_formula(ctrl)
    elif chart_name == "条带图":
        display_formula(ctrl)
    else:
        MsgBox(f"未定义的图表类型 {chart_name}")


def get_gallery_2_count(ctrl):
    return len(gallery_2_images)


def get_gallery_2_label(ctrl, index: int):
    return gallery_2_images[index]["chart_name"]


def get_gallery_2_image(ctrl, index: int):
    image_path = (
        Path(os.path.join(sys.prefix, "share", "zhixinpy"))
        / gallery_2_images[index]["file_name"]
    )
    if not image_path.exists():
        return Image.new("RGB", (1, 1), (0, 0, 0))
    img  = Image.open(image_path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")  # 转换为 RGB 模式
    return img


def on_gallery_2_action(ctrl, galleryid: str, index: int):
    chart_name = gallery_2_images[index]["chart_name"]
    if chart_name == "散点图":
        show_scatter_dialog(ctrl)
    elif chart_name == "三维散点图":
        show_scatter3d_dialog(ctrl)
    elif chart_name == "桑基图":
        show_sankey_dialog(ctrl)
    elif chart_name == "桑基图(财报)":
        show_sankey_financial_dialog(ctrl)
    elif chart_name == "矩形树图":
        show_treemap_dialog(ctrl)
    elif chart_name == "旭日图":
        show_sunburst_dialog(ctrl)
    elif chart_name == "网络图":
        show_network_dialog(ctrl)
    else:
        MsgBox(f"未定义的图表类型 {chart_name}")


def get_gallery_3_count(ctrl):
    return len(gallery_3_images)


def get_gallery_3_label(ctrl, index: int):
    return gallery_3_images[index]["chart_name"]


def get_gallery_3_image(ctrl, index: int):
    image_path = (
        Path(os.path.join(sys.prefix, "share", "zhixinpy"))
        / gallery_3_images[index]["file_name"]
    )
    if not image_path.exists():
        return Image.new("RGB", (1, 1), (0, 0, 0))
    img  = Image.open(image_path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")  # 转换为 RGB 模式
    return img


def on_gallery_3_action(ctrl, galleryid: str, index: int):
    chart_name = gallery_3_images[index]["chart_name"]
    if chart_name == "地图":
        show_map_dialog(ctrl)
    elif chart_name == "地图散点图":
        display_formula(ctrl)
    elif chart_name == "地图路径图":
        display_formula(ctrl)
    elif chart_name == "坐标图":
        show_geo_dialog(ctrl)
    elif chart_name == "坐标路线图":
        show_geoline_dialog(ctrl)
    elif chart_name == "地图柱状图":
        show_map_bar_dialog(ctrl)
    else:
        MsgBox(f"未定义的图表类型 {chart_name}")


def get_gallery_4_count(ctrl):
    return len(gallery_4_images)


def get_gallery_4_label(ctrl, index: int):
    return gallery_4_images[index]["chart_name"]


def get_gallery_4_image(ctrl, index: int):
    image_path = (
        Path(os.path.join(sys.prefix, "share", "zhixinpy"))
        / gallery_4_images[index]["file_name"]
    )
    if not image_path.exists():
        return Image.new("RGB", (1, 1), (0, 0, 0))
    img  = Image.open(image_path)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")  # 转换为 RGB 模式
    return img


def on_gallery_4_action(ctrl, galleryid: str, index: int):
    chart_name = gallery_4_images[index]["chart_name"]
    if chart_name == "3D曲面图":
        show_surface3d_dialog(ctrl)
    elif chart_name == "饼状柱状图":
        show_pie_bar_dialog(ctrl)
    elif chart_name == "3D柱状图":
        show_bar3d_dialog(ctrl)
    elif chart_name == "排名图":
        show_rank_dialog(ctrl)
    elif chart_name == "排名图(Wind)":
        show_rank_wind_dialog(ctrl)
    elif chart_name == "词云图":
        show_wordcloud_dialog(ctrl)
    elif chart_name == "日历热力图":
        show_heatmap_dialog(ctrl)
    elif chart_name == "K线图":
        show_kchart_dialog(ctrl)
    else:
        MsgBox(f"未定义的图表类型{chart_name}")


def display_formula(ctrl):
    function_name = ctrl.tag
    func = globals().get(function_name)
    if func:
        msg = func.__doc__
    else:
        msg = f"函数{function_name}不存在"
    MsgBox(msg)


_ribbon_ui = xlo.ExcelGUI(
    ribbon=rf"""
<customUI
	xmlns="http://schemas.microsoft.com/office/2009/07/customui">
	<ribbon>
		<tabs>
			<tab id="tab1" label="❤️知心❤️" insertAfterMso="TabHome">
                <group id="funcGroup" label="知心函数">
					<button id="env-2" size="large" label="预加载函数" onAction="preLoad" imageMso="FunctionWizard" screentip="预载入所有知心函数" supertip="预载入后，所有知心函数可以丝滑调用，不需要额外的等待执行时间。" />
					<menu id="toolMenu" size="large" label="工具" imageMso="ControlToolboxOutlook" itemSize="normal">
						<button id="tool1" label="生成二维码" imageMso="PivotTableSelectData" onAction="show_qrcode_dialog" tag="zt_Qrcode" screentip="用于生成和解析二维码的功能"/>
						<button id="tool2" label="图片下载" imageMso="PictureInsertFromFile" onAction="show_image_dialog" tag="zt_Image" screentip="支持图像加载、格式转换和基础处理操作"/>
						<button id="tool3" label="视频下载" imageMso="ToolboxVideo" onAction="show_video_dialog" tag="zt_Video" screentip="实现视频编解码和基础剪辑功能"/>
						<button id="tool4" label="文件下载" imageMso="FileSave" onAction="show_download_dialog" tag="zt_Download" screentip="支持多线程文件下载和断点续传"/>
						<button id="tool5" label="发送邮件" imageMso="SendStatusReport" onAction="show_mail_dialog" tag="zt_Mail" screentip="提供SMTP邮件发送和接收功能"/>
						<button id="tool9" label="爬虫" imageMso="HyperlinkInsert" onAction="show_crawler_dialog" tag="zt_Crawler" screentip="单页面内容抓取和解析工具"/>
						<button id="tool11" label="公钥生成" imageMso="Lock" onAction="show_genpubkey_dialog" tag="zt_GenPubKey" screentip="生成RSA/ECC非对称加密公钥"/>
						<button id="tool12" label="数据加密" imageMso="FileDocumentEncrypt" onAction="show_encrypt_dialog" tag="zt_Encrypt" screentip="支持AES/DES对称加密算法"/>
						<button id="tool13" label="数据解密" imageMso="EncryptMessage" onAction="show_decrypt_dialog" tag="zt_Decrypt" screentip="解密已加密的文件和数据流"/>
						<button id="tool14" label="文字转语音" imageMso="SoundInsertFromFile" onAction="show_tts_dialog" tag="zt_tts" screentip="将文本转换为自然语音输出"/>
						<button id="tool15" label="桌面通知" imageMso="_3DLightingClassic" onAction="show_notice_dialog" tag="zt_Notice" screentip="发送桌面和移动端推送通知"/>
						<button id="tool16" label="视频格式转换" imageMso="OmsNewMultimediaMessage" onAction="show_convert_media_dialog" tag="zt_Convert_Media" screentip="支持音视频格式互转和压缩"/>
                        <button id="tool17" label="身份证提取" imageMso="OmsNewMultimediaMessage" onAction="show_idcard_dialog" tag="zt_IDCard" screentip="身份证提取"/>
                        <button id="tool18" label="银行卡校验" imageMso="OmsNewMultimediaMessage" onAction="show_bankcard_dialog" tag="zt_BankCard" screentip="银行卡校验"/>
                    </menu>
                    <menu id="aiMenu" size="large" label="AI" imageMso="NewDistributionList" itemSize="normal">
                        <button id="ai1" label="大语言模型" imageMso="HappyFace" onAction="show_llm_dialog" tag="zt_LLM" screentip="基础自然语言处理接口"/>
						<button id="ai2" label="仿照推理" imageMso="HappyFace" onAction="show_llmex_dialog" tag="zt_LLMEx" screentip="支持自定义模型的扩展接口"/>
						<button id="ai3" label="生成同类" imageMso="HappyFace" onAction="show_llmgen_dialog" tag="zt_LLMGen" screentip="实现AI文本生成和续写功能"/>
                        <button id="ai4" label="翻译" imageMso="HappyFace" onAction="show_llm_translate_dialog" tag="zt_LLM_translate" screentip="实现AI文本生成和续写功能"/>
                        <button id="ai5" label="分类" imageMso="HappyFace" onAction="show_llm_categorize_dialog" tag="zt_LLM_categorize" screentip="实现AI文本生成和续写功能"/>
                        <button id="ai6" label="提取" imageMso="HappyFace" onAction="show_llm_extract_dialog" tag="zt_LLM_extract" screentip="实现AI文本生成和续写功能"/>
                        <button id="ai7" label="润色" imageMso="HappyFace" onAction="show_llm_rewrite_dialog" tag="zt_LLM_rewrite" screentip="实现AI文本生成和续写功能"/>
                    </menu>
					<menu id="dateMenu" size="large" label="日期" imageMso="ContentControlDate">
						<menu id="date1" label="期基础信息类" imageMso="Chart3DColumnChart" itemSize="normal">
							<button id="date1-1" label="月天数" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_days_in_month" screentip="获取某个月的天数（例如，2月28天或29天）"/>
							<button id="date1-2" label="年天数" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_days_in_year" screentip="获取一年中的天数，通常为365天或366天（闰年）"/>
							<button id="date1-3" label="星期几" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_day_of_week" screentip="获取某一天是星期几（如周一、周二等）"/>
						</menu>
						<menu id="date2" label="日期/周信息类" imageMso="Chart3DColumnChart" itemSize="normal">
							<button id="date2-1" label="月周数" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_week_of_month" screentip="获取某日期在当前月份是第几周"/>
							<button id="date2-2" label="年周数" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_week_of_year" screentip="获取某日期在当前年份是第几周"/>
							<button id="date2-3" label="季度信息" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_quarter_of_year" screentip="获取某日期所属的季度（第一季度，第二季度等）"/>
						</menu>
						<menu id="date3" label="日期转换类" imageMso="Chart3DColumnChart" itemSize="normal">
							<button id="date3-1" label="时间戳转日期" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_EpochToDate" screentip="将Unix时间戳（秒或毫秒）转换为具体的日期" />
							<button id="date3-2" label="日期差异" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zd_DateDif" screentip="计算两个日期之间的天数差异（例如，开始日期和结束日期的天数差异）" />
						</menu>
					</menu>
					<menu id="convertMenu" size="large" label="转换" imageMso="PivotTableOlapConvertToFormulas" itemSize="normal">
						<button id="convert1" label="转换为大写" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zv_to_uppercase" screentip="将字符串中的所有字母转换为大写字母"/>
						<button id="convert2" label="转换为小写" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zv_to_lowercase" screentip="将字符串中的所有字母转换为小写字母"/>
						<button id="convert3" label="首字母大写" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zv_tcapitalize_first_letter" screentip="将字符串的第一个字母转换为大写，其余部分保持原样"/>
						<button id="convert4" label="每个单词首字母大写" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zv_capitalize_each_word" screentip="将字符串中每个单词的首字母转换为大写，其余部分保持原样"/>
						<button id="convert5" label="去除空格" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zv_strip_spaces" screentip="去除字符串两端的空格"/>
						<button id="convert6" label="转换为日期" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zv_to_date" screentip="将字符串或时间戳转换为日期格式"/>
					</menu>
					<menu id="filterMenu" size="large" label="过滤" imageMso="AutoFilterClassic" itemSize="normal">
						<button id="filter1" label="排序" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zf_Sort" screentip="排序"/>
						<button id="filter2" label="新排序" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zf_SortN" screentip="新排序"/>
						<button id="filter3" label="去重" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zf_Unique" screentip="去重"/>
					</menu>
					<menu id="seriesMenu" size="large" label="序列" imageMso="ChartFormatDataLabels" itemSize="normal">
						<button id="series1" label="FillWithCS" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zs_FillWithCS" screentip="FillWithCS"/>
						<button id="series2" label="zs_FillWithKNN" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zs_FillWithKNN" screentip="zs_FillWithKNN"/>
						<button id="series3" label="zs_SeasonalDecompose" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zs_SeasonalDecompose" screentip="zs_SeasonalDecompose"/>
						<button id="series4" label="zs_Prophet" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zs_Prophet" screentip="zs_Prophet"/>
						<button id="series5" label="zs_MinIfs" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zs_MinIfs" screentip="zs_MinIfs"/>
						<button id="series6" label="zs_MaxIfs" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zs_MaxIfs" screentip="zs_MaxIfs"/>
					</menu>
					<menu id="lookupMenu" size="large" label="查找" imageMso="DatasheetColumnLookup" itemSize="normal">
						<button id="lookup1" label="自然语言查找" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zl_NlpLookup" screentip="自然语言查找"/>
						<button id="lookup2" label="XLookup" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zl_XLookup" screentip="XLookup"/>
					</menu>
					<menu id="textMenu" size="large" label="文本" imageMso="TextBoxInsert" itemSize="normal">
						<button id="text1" label="是否日期" imageMso="CalendarInsert"   onAction="display_formula" tag="ze_IsDate" screentip="日期校验" supertip="验证输入是否为有效日期格式" />
						<button id="text2" label="是否邮箱" imageMso="SendCopySendNow"   onAction="display_formula" tag="ze_IsEmail" screentip="邮箱校验" supertip="验证输入是否符合邮箱格式规范" />
						<button id="text3" label="正则提取" imageMso="FunctionInsertGallery"   onAction="display_formula" tag="ze_RegexExtract" screentip="正则提取" supertip="使用正则表达式提取特定模式的文本" />
						<button id="text4" label="正则匹配" imageMso="CheckMark"   onAction="display_formula" tag="ze_RegexMatch" screentip="模式匹配" supertip="判断文本是否符合指定正则模式" />
						<button id="text5" label="正则替换" imageMso="ReplaceDialog"   onAction="display_formula" tag="ze_RegexReplace" screentip="模式替换" supertip="使用正则表达式进行批量文本替换" />
						<button id="text6" label="分割文本" imageMso="TableSplitTable"   onAction="display_formula" tag="ze_Split" screentip="文本分割" supertip="按指定分隔符拆分字符串为数组" />
						<button id="text7" label="合并文本" imageMso="MergeCells"   onAction="display_formula" tag="ze_Join" screentip="文本合并" supertip="将数组元素合并为单一字符串" />
						<button id="text8" label="是否URL" imageMso="HyperlinkInsert"   onAction="display_formula" tag="ze_IsURL" screentip="链接校验" supertip="验证输入是否为有效URL地址" />
						<button id="text9" label="透视分组" imageMso="PivotTableWizard"   onAction="display_formula" tag="ze_PivotBy" screentip="数据透视" supertip="按指定字段进行数据透视分组" />
						<button id="text10" label="数据聚合" imageMso="AutoSum"   onAction="display_formula" tag="ze_GroupBy" screentip="数据聚合" supertip="按指定条件对数据进行分组统计" />
					</menu>
					<menu id="quoteMenu" size="large" label="行情" imageMso="DollarSign" itemSize="normal">
						<button id="quote1" label="实时行情" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zq_Realtime" screentip="zq_Realtime" supertip="返回实时行情"/>
						<button id="quote2" label="分钟行情" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zq_MinuteK" screentip="zq_MinuteK" supertip="返回分钟行情"/>
						<button id="quote3" label="日行情" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zq_DailyK" screentip="zq_DailyK" supertip="返回日行情"/>
						<button id="quote4" label="周行情" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zq_WeeklyK" screentip="zq_WeeklyK" supertip="返回周行情"/>
						<button id="quote5" label="月行情" imageMso="ChartTypeBarInsertGallery" onAction="display_formula" tag="zq_MinuteK" screentip="zq_MinuteK" supertip="返回月行情"/>
					</menu>
				</group>
                <group id="chartGroup" label="知心图表">
                    <gallery id="chart1" imageMso="ChartTypeBarInsertGallery" label="基础图表" size="large"
                        columns="2" rows="4" itemWidth="240" itemHeight="180"
                        getItemCount="get_gallery_1_count"
                        getItemLabel="get_gallery_1_label"
                        getItemImage="get_gallery_1_image"
                        onAction="on_gallery_1_action" />
                    <gallery id="chart2" imageMso="ChartTypeXYScatterInsertGallery" label="关系与分布" size="large"
                        columns="2" rows="4" itemWidth="240" itemHeight="180"
                        getItemCount="get_gallery_2_count"
                        getItemLabel="get_gallery_2_label"
                        getItemImage="get_gallery_2_image"
                        onAction="on_gallery_2_action" />
                    <gallery id="chart3" imageMso="CreateMap" label="地理与空间" size="large"
                        columns="2" rows="4" itemWidth="240" itemHeight="180"
                        getItemCount="get_gallery_3_count"
                        getItemLabel="get_gallery_3_label"
                        getItemImage="get_gallery_3_image"
                        onAction="on_gallery_3_action" />
                    <gallery id="chart4" imageMso="ChartSecondaryVerticalGridlines" label="高级图表" size="large"
                        columns="2" rows="4" itemWidth="240" itemHeight="180"
                        getItemCount="get_gallery_4_count"
                        getItemLabel="get_gallery_4_label"
                        getItemImage="get_gallery_4_image"
                        onAction="on_gallery_4_action" />
                </group>
				<group id="quick" autoScale="false" centerVertically="false" label="快速">
					<button id="quick-1" label="截图" imageMso="WordPicture" onAction="capture" screentip="截图" supertip="如果没选中图形，则截取工作页所有图形；如果选中了某些图形，则截取所选的图形" />
					<button id="quick-2" label="重排图表" imageMso="PrintPreviewMultiplePagesMenu" onAction="reorganize_charts" screentip="重排图表" supertip="按照指定规则重新排列当前工作表中的图表位置。" />
					<button id="quick-3" label="创建目录" imageMso="CategoryCollapse" onAction="create_index_sheet" screentip="创建目录表" supertip="创建新的目录表并添加每个工作表的超链接。" />
					<button id="quick-5" label="条件格式" imageMso="FontConditionalFormatting" onAction="create_condition_format_b_column" screentip="条件格式" supertip="为B列及2行设置条件格式，根据单元格内容改变背景色和字体样式。支持tt/t/1/2/3/4/5/6/u/i/b" />
				</group>
				<group id="file" autoScale="false" centerVertically="false" label="文件管理">
					<button id="file-1" label="取所有文件" imageMso="FileOpenDatabase" onAction="tree" screentip="取所有文件" supertip="选择某一目录，递归取得该目录下所有文件" />
					<button id="file-2" label="取当前目录" imageMso="FileOpenDatabase" onAction="treedir" screentip="取所选目录下的文件或目录" supertip="选择某一目录，取得该目录下的所有文件" />
					<button id="file-3" label="批量重命名" imageMso="SlideMasterRenameMaster" onAction="rename" screentip="批量重命名" supertip="可以批量重命名所选的多个文件" />
					<button id="file-4" label="合并工作薄" imageMso="MailMergeMatchFields" onAction="mergeBooks" screentip="合并工作薄" supertip="合并多个工作薄中的首个sheet，适合用在从各处收集sheet并汇总" />
				</group>
				<group id="env" autoScale="false" centerVertically="false" label="知心配置">
					<button id="env-1" size="large" label="配置参数" imageMso="DatabaseEncodeDecode" onAction="show_config_dialog" screentip="配置" supertip="配置知心的一些参数" />
					<menu id="helpmenu" size="large" label="帮助" imageMso="Help">
						<button id="env-3" label="关于知心" onAction="OnAboutButtonClick" imageMso="Info" />
						<button id="env-8" label="访问官网" imageMso="HappyFace" onAction="open_website" />
						<button id="env-5" label="日志文件" imageMso="ZoomCurrent75" onAction="press_open_log" screentip="打开日志文件" supertip="里面有函数调用的详细细节，包括函数调用报错信息，如果发现问题，可把该日志文件发送到zhixin_excel@163.com帮您排查" />
						<button id="env-6" label="注册流程" imageMso="DatabaseEncodeDecode" onAction="show_registration_dialog" screentip="注册流程" supertip="注册流程的提示" />
						<button id="env-7" label="导入注册码" imageMso="AdpPrimaryKey" onAction="load_register_file" screentip="载入注册码zhixinpy.lic" supertip="联系zhixin_excel@163.com获得注册码文件zhixinpy.lic后，通过本按钮导入，之后点“关于知心”查看是否更新了注册信息" />
					</menu>
				</group>
			</tab>
		</tabs>
	</ribbon>
</customUI>
    """,
    funcmap=_ribbon_func_map,
)


############################### FUNCTION  START ##############################################


#################################   func_calendar    #########################################


@xlo.func(
    group="知心-日期",
    args={
        "date": "【日期，数字或字符串，默认今天】可以是你想到的所有表示日期的格式。例如 20240101 2024-01-01 2024/01/01 2024/1/1 2024-1-1 等等"
    },
)
@catch_and_log(return_type="na")
def zd_days_in_month(date="default"):
    """这天所在月份有几天
    示例：
        =zd_days_in_month("20250101") -> 31
        =zd_days_in_month(2026/1/1)  -> 31"""
    from zhixinpy import func_calendar

    if date == "default":
        date = dt.datetime.now().strftime("%Y%m%d")
    return func_calendar.days_in_month(thedate=date)


@xlo.func(
    group="知心-日期",
    args={
        "date": "【日期，数字或字符串，默认今天】可以是你想到的所有表示日期的格式。例如 20240101 2024-01-01 2024/01/01 2024/1/1 2024-1-1 等等"
    },
)
@catch_and_log(return_type="na")
def zd_days_in_year(date="default"):
    """这天所在的年份有几天
    示例：
        =zd_days_in_year("20250101") -> 365
        =zd_days_in_year(2020/1/1)  -> 366"""
    from zhixinpy import func_calendar

    if date == "default":
        date = dt.datetime.now().strftime("%Y%m%d")
    return func_calendar.days_in_year(thedate=date)


@xlo.func(
    group="知心-日期",
    args={
        "date": "【日期，数字或字符串，默认今天】可以是你想到的所有表示日期的格式。例如 20240101 2024-01-01 2024/01/01 2024/1/1 2024-1-1 等等"
    },
)
@catch_and_log(return_type="na")
def zd_day_of_week(date="default"):
    """这天是本周第几天。周一返回1，周日返回7
    示例：
        =zd_day_of_week("20250101") -> 3
        =zd_day_of_week(2026/1/1)  -> 4"""
    from zhixinpy import func_calendar

    if date == "default":
        date = dt.datetime.now().strftime("%Y%m%d")
    return func_calendar.day_of_week(thedate=date)


@xlo.func(
    group="知心-日期",
    args={
        "date": "【日期，数字或字符串，默认今天】可以是你想到的所有表示日期的格式。例如 20240101 2024-01-01 2024/01/01 2024/1/1 2024-1-1 等等"
    },
)
@catch_and_log(return_type="na")
def zd_week_of_month(date="default"):
    """这天是本月的第几周
    示例：
        =zd_week_of_month("20250101") -> 1
        =zd_week_of_month(2026/1/1)  -> 1"""
    from zhixinpy import func_calendar

    if date == "default":
        date = dt.datetime.now().strftime("%Y%m%d")
    return func_calendar.week_of_month(thedate=date)


@xlo.func(
    group="知心-日期",
    args={
        "date": "【日期，数字或字符串，默认今天】可以是你想到的所有表示日期的格式。例如 20240101 2024-01-01 2024/01/01 2024/1/1 2024-1-1 等等"
    },
)
@catch_and_log(return_type="na")
def zd_week_of_year(date="default"):
    """这天是该年第几周。一年有53或54周。
    注意这里的小坑：往往元旦或元旦之后几天属于去年的最后一周，所以用时要结合该日期的年份
    示例：
        =zd_week_of_year("20250101") -> 1
        =zd_week_of_year(2026/1/1)  -> 53"""
    from zhixinpy import func_calendar

    if date == "default":
        date = dt.datetime.now().strftime("%Y%m%d")
    return func_calendar.week_of_year(thedate=date)


@xlo.func(
    group="知心-日期",
    args={
        "date": "【日期，数字或字符串，默认今天】可以是你想到的所有表示日期的格式。例如 20240101 2024-01-01 2024/01/01 2024/1/1 2024-1-1 等等"
    },
)
@catch_and_log(return_type="na")
def zd_quarter_of_year(date="default"):
    """这天是该年第几季。1月1日至3月31日为第一季返回1
    示例：
        =zd_quarter_of_year("20250101") -> 1
        =zd_quarter_of_year(2026/4/1)  -> 2"""
    from zhixinpy import func_calendar

    if date == "default":
        date = dt.datetime.now().strftime("%Y%m%d")
    return func_calendar.quarter_of_year(thedate=date)


@xlo.func(
    group="知心-日期",
    args={
        "timestamp": "Unix 纪元时间戳（以秒、毫秒或微秒为单位）。",
        "time_unit": "用于表示时间戳的时间单位。1（默认值）表示时间单位是秒。2表示时间单位是毫秒。3表示时间单位是微秒。",
    },
)
@catch_and_log(return_type="na")
@formatter(number_format="yyyy/mm/dd")
def zd_EpochToDate(timestamp, time_unit=1):
    """将 Unix 纪元时间戳（以秒、毫秒或微秒为单位）转换为世界协调时间 (UTC) 的日期时间。
    示例：
        =zd_EpochToDate(1655906568893, 2) -> "2022-06-22 12:02:48" """
    from zhixinpy import func_calendar

    return func_calendar.epochToDate(timestamp=timestamp, time_unit=time_unit)


@xlo.func(
    group="知心-日期",
    args={
        "start_date": "计算中要使用的开始日期。必须是对包含DATE值的单元格的引用、返回DATE类型的函数或数字。",
        "end_date": "计算中要使用的结束日期。必须是对包含DATE值的单元格的引用、返回DATE类型的函数或数字。",
        "unit": "时间单位的缩写文字。例如 'M' 代表月。有效值包括：'Y'、'M'、'D'、'MD'、'YM' 和 'YD'。",
    },
)
@catch_and_log(return_type="na")
def zd_DateDif(start_date, end_date, unit: str = "D"):
    """计算两个日期之间的天数、月数或年数。
    示例：
        =zd_DateDif(DATE(1969, 7, 16), DATE(1969, 7, 24), "D") -> 8"""
    from zhixinpy import func_calendar

    return func_calendar.dateDif(start_date=start_date, end_date=end_date, unit=unit)


#################################   func_converter   #########################################


@xlo.func(
    group="知心-转换",
    args={"text": "【文本，字符串，默认空串】待转成大写的文本"},
)
@catch_and_log(return_type="na")
def zv_to_uppercase(text=""):
    """将文本中的字母全部转换为大写形式，保留非字母字符不变
    示例：
        =zv_to_uppercase("hello 123") -> "HELLO 123"
        =zv_to_uppercase("AbC测试")  -> "ABC测试"
    """
    from zhixinpy import func_converter

    return func_converter.to_uppercase(text)


@xlo.func(
    group="知心-转换",
    args={"text": "【文本，字符串，默认空串】待转成小写的文本"},
)
@catch_and_log(return_type="na")
def zv_to_lowercase(text=""):
    """将文本中的字母全部转换为小写形式，保留非字母字符不变
    示例：
        =zv_to_lowercase("HELLO 123") -> "hello 123"
        =zv_to_lowercase("AbC测试")  -> "abc测试"
    """
    from zhixinpy import func_converter

    return func_converter.to_lowercase(text)


@xlo.func(
    group="知心-转换",
    args={"text": "【文本，字符串，默认空串】"},
)
@catch_and_log(return_type="na")
def zv_tcapitalize_first_letter(text=""):
    """文本中，仅仅把句首字母转成大写，保留其他字符不变
    示例：
        =zv_tcapitalize_first_letter("hello world") -> "Hello world"
        =zv_tcapitalize_first_letter("python programming") -> "Python programming"
    """
    from zhixinpy import func_converter

    return func_converter.capitalize_first_letter(text)


@xlo.func(
    group="知心-转换",
    args={"text": "【文本，字符串，默认空串】"},
)
@catch_and_log(return_type="na")
def zv_capitalize_each_word(text=""):
    """文本中，将以空格分隔的每个单词的首字母转成大写，其余字符保持不变
    示例：
        =zv_capitalize_each_word("hello world") -> "Hello World"
        =zv_capitalize_each_word("python   programming") -> "Python   Programming"
    """
    from zhixinpy import func_converter

    return func_converter.capitalize_each_word(text)


@xlo.func(
    group="知心-转换",
    args={"text": "【文本，字符串，默认空串】"},
)
@catch_and_log(return_type="na")
def zv_strip_spaces(text=""):
    """文本中，去掉首尾的空格，保留中间的空格不变
    示例：
        =zv_strip_spaces("  hello world  ") -> "hello world"
        =zv_strip_spaces("  python programming  ") -> "python programming"
    """
    from zhixinpy import func_converter

    return func_converter.strip_spaces(text)


@xlo.func(
    group="知心-转换",
    args={"text": "【文本，字符串，默认空串】"},
)
@catch_and_log(return_type="na")
@formatter(number_format="yyyy/mm/dd")
def zv_to_date(text=""):
    """把它转成Excel日期
    示例：
        =zv_to_date("20200101") -> 2020/1/1
        =zv_to_date(20200101) -> 2020/1/1
        =zv_to_date("2020-01-01") -> 2020/1/1
    """
    from zhixinpy import func_converter

    return func_converter.to_date(text)


#################################   func_filter   #########################################


@xlo.func(
    group="知心-过滤器",
    args={
        "excel_range": "要排序的数据。",
        "sort_column": "范围内或范围之外的某个范围中的某列的列号，该列中的值指定了排序顺序。",
        "ascending": "取 TRUE 或 FALSE，指示是否将排序依据列按升序排序。FALSE 表示按降序排序。",
        "sort_column2": "首列之外的其他列和排序顺序标志，请将优先程度高的列放在前面。（可选）",
        "ascending2": "第二排序列是否按升序排序。（可选）",
    },
)
@catch_and_log(return_type="na")
def zf_Sort(
    excel_range, sort_column, ascending=True, sort_column2=None, ascending2=True
):
    """依据一列或多列中的值对数组或范围中的行进行排序
    示例：
    =zf_Sort(A2, 1, TRUE) -> 按首列升序排列的二维数组
    =zf_Sort(C2, 3, FALSE, 2, TRUE) -> 优先按第三列降序、第二列升序排列的结果"""
    from zhixinpy import func_filter

    return func_filter.sort(
        excel_range=excel_range,
        sort_column=sort_column,
        ascending=ascending,
        sort_column2=sort_column2,
        ascending2=ascending2,
    )


@xlo.func(
    group="知心-过滤器",
    args={
        "excel_range": "要对其进行排序并找到前 n 个项目的数据。",
        "n": "要返回的项目数量，必须大于 0。",
        "mode": "表示相同的值的显示方式的数字。0：最多显示已排序范围中的前 n 行。1：最多显示前 n 行，以及与第 n 行相同的其他行。2：移除重复的行后，最多显示前 n 行。3：最多显示前 n 个不重复行，但显示这些行的每个重复行。",
        "sort_column1": "在范围中或在范围以外的范围中列（包含要排序的值）的编号。指定为排序列1 的范围必须是行数与范围相同的单个列。",
        "ascending1": "指示如何对排序列1排序。TRUE 表示按升序排序，FALSE 表示按降序排序。",
        "sort_column2": "出现相同的值时使用的附加列（优先程度从高到低）。（可选）",
        "ascending2": "指示如何对排序列2排序。（可选）",
    },
)
@catch_and_log(return_type="na")
def zf_SortN(
    excel_range,
    n=1,
    mode=0,
    sort_column1=None,
    ascending1=True,
    sort_column2=None,
    ascending2=True,
):
    """返回排序后数据集中的前 n 个项目
    示例：
    =zf_SortN(A1, 2) -> 前2个最小数值
    =zf_SortN(B2, 3, 1) -> 包含与第三项相同值的所有条目"""
    from zhixinpy import func_filter

    return func_filter.sortN(
        excel_range=excel_range,
        n=n,
        mode=mode,
        sort_column1=sort_column1,
        ascending1=ascending1,
        sort_column2=sort_column2,
        ascending2=ascending2,
    )


@xlo.func(
    group="知心-过滤器",
    args={
        "excel_range": "要按唯一性原则进行过滤的数据。",
        "by_column": "是否要按列或行进行过滤。默认情况下，值为 false。",
        "exactly_once": "是否仅返回不重复的条目。默认情况下，值为 false。",
    },
)
@catch_and_log(return_type="na")
def zf_Unique(excel_range, by_column=False, exactly_once=False):
    """返回源范围中具有唯一性的行并剔除重复行
    示例：
    =zf_Unique([[1,2],[1,2],[3,4]]) -> [[1,2],[3,4]]
    =zf_Unique(A1, exactly_once=True) -> 仅出现一次的记录"""
    from zhixinpy import func_filter

    return func_filter.unique(
        excel_range=excel_range, by_column=by_column, exactly_once=exactly_once
    )


#################################   func_lookup    #########################################


@xlo.func(
    group="知心-查找",
    args={
        "lookup_value": "【待查找的值，数字或字符串，默认空】跟VLOOKUP一样，填待查找的值",
        "table_array": "【数据矩阵，矩阵，默认空】跟VLOOKUP一样，填需要搜索的数据表，其中第一列为搜索的KEY",
        "col_index_num": "【查找结果列号，数字，默认空，非必填】`table_array`中需要查找出来的列号",
        "include_score": "【是否返回分数，数字，默认False，非必填】是否返回分数",
        "all_matches": "【是否全匹配，数字，默认False，非必填】是否全匹配",
        "threshold": "【阈值，数字，默认0.5，非必填】阈值",
        "tokenizer_type": "【中文分词引擎，字符串，默认空，非必填】中文分词引擎。默认情况下搜索传长度不超过4则用单字做分词，否则用jieba做语义分词。输入jieba则全用jieba分词，输入char则用单字分词",
    },
)
def zl_NlpLookup(
    lookup_value=None,
    table_array=None,
    col_index_num: int = 0,
    include_score=False,
    all_matches=False,
    threshold=0.3,
    tokenizer_type="",
) -> PDFrame(headings=False, index=False):
    """示例
        =zl_NlpLookup(I4,D:E,1)

    简介
        智能VLOOKUP
        与 EXCEL 中的 VLOOKUP 函数用法类似，但使用自然语言处理模型进行分词和查找，从而获得更精准的语义搜索结果。

    参数：
        lookup_value：待查找的值，可以是数字或字符串，类似于 VLOOKUP 函数中的查找值。
        table_array：数据矩阵，类似于 VLOOKUP 函数中的查找范围，其中第一列为搜索的关键列。
        col_index_num：查找结果列号，指定返回结果所在的列，类似于 VLOOKUP 函数中的第三个参数。
        include_score：是否返回匹配分数，如果为 True，则会返回找到的结果的匹配得分。
        all_matches：是否全匹配，如果为 True，则只返回完全匹配的结果，否则返回模糊匹配的结果。
        threshold：阈值，用于控制匹配的灵敏度，阈值越高，匹配越严格。
        tokenizer_type：中文分词引擎，可以选择不同的分词引擎来提高搜索精度，例如 jieba 或 char。
    """
    from zhixinpy import func_lookup

    return func_lookup.nlp_vlookup(
        lookup_value=lookup_value,
        table_array=table_array,
        col_index_num=col_index_num,
        include_score=include_score,
        all_matches=all_matches,
        threshold=threshold,
        tokenizer_type=tokenizer_type,
    )


@xlo.func(
    group="知心-查找",
    args={
        "search_key": "要搜索的值。",
        "lookup_range": "要搜索的范围。此范围必须为单行或单列。",
        "result_range": "结果值所在的范围。此范围的行数或列数应与 lookup_range 相同，具体取决于查询方式。",
        "missing_value": "[可选 - 默认值为 #N/A] 如果未找到匹配值，则返回此值。",
        "match_mode": "[可选 - 默认值为 0] 查找 search_key 匹配值的方式。",
        "search_mode": "[可选 - 默认值为 1] 搜索 lookup_range 的方式。",
    },
)
@catch_and_log(return_type="na")
def zl_XLookup(
    search_key,
    lookup_range,
    result_range,
    missing_value=None,
    match_mode=0,
    search_mode=1,
):
    """用法示例
    =zl_XLookup("Apple", A2:A, E2:E) 用于取代 VLOOKUP("Apple", A2:E, 5, FALSE)
    =zl_XLookup("Price", A1:E1, A6:E6) 用于取代 HLOOKUP("Price", A1:E6, 6, FALSE)
    =XLOOKUP，其中的匹配值列位于输出列的右侧
    =XLOOKUP("Apple", E2:E7, A2:A7)。等效的 VLOOKUP 函数是 VLOOKUP("Apple", {E2:E7, A2:A7}, 2, FALSE)
    """
    from zhixinpy import func_lookup

    return func_lookup.xLookup(
        search_key=search_key,
        lookup_range=lookup_range,
        result_range=result_range,
        missing_value=missing_value,
        match_mode=match_mode,
        search_mode=search_mode,
    )


#################################   ZS 获得序列    #########################################


@xlo.func(
    group="知心-序列",
    args={
        "arr": "目标数列，包含需要填充缺失值的数列",
    },
)
def zs_FillWithCS(arr: xlo.Array()):
    """利用三次样条插值法，填充表格数据中日期列和数据列的缺失值。
    示例
        =zs_FillWithCS(E2:E8)
    """
    from zhixinpy import func_series

    return func_series.fill_with_cs(arr=arr)


@xlo.func(
    group="知心-序列",
    args={
        "arr1": "参考数列，包含完整数据，用于提供填充参考",
        "arr2": "目标数列，包含需要填充缺失值的数列",
        "n_neighbors": "KNN 算法中使用的邻居数量，默认为3",
    },
)
def zs_FillWithKNN(arr1: xlo.Array(), arr2: xlo.Array(), n_neighbors=3):
    """使用 KNN 算法填充缺失值根据参考表格 arr1，利用 KNN 算法填充目标表格 arr2 中的缺失值。
    示例
        =zs_FillWithKNN(D2:D8, E2:E8)
        =zs_FillWithKNN(D2:D8, E2:E8, 4)
    """
    arr1_flat = np.array(arr1.flatten(), dtype=float)
    arr2_flat = np.array(arr2.flatten(), dtype=float)
    if len(arr1_flat) != len(arr2_flat):
        return "错误：arr1和arr2长度必须一样"
    if n_neighbors <= 0:
        return "错误：n_neighbors必须是正整数"
    from zhixinpy import func_series

    return func_series.fill_with_knn(arr1=arr1, arr2=arr2, n_neighbors=n_neighbors)


@xlo.func(
    group="知心-序列",
    args={
        "data": "带表头的表格",
        "ds": "【日期轴字段名，字符串，默认空】日期轴字段",
        "y": "【数据轴字段名，字符串，默认是】数据轴字段",
        "period": "[可选]【周期，数值，默认是12】季节性周期长度，对于年周期为365，月周期为12，",
    },
)
def zs_SeasonalDecompose(data: xlo.Array(), ds, y, period=12):
    """将时间序列数据分解为趋势成分、季节性成分和残差成分，用于分析数据的周期性规律。
    示例
        =zs_SeasonalDecompose(B2:C59,B2,C2)
    """
    if not (data.shape[0] > 1 and data.shape[1] > 1):
        return "错误：选取的区域必须是表格"
    if not any(isinstance(item, str) for item in data[0]):
        return "错误：选取的区域请包含表格头"
    if ds not in data[0]:
        return "错误：指定的日期字段名不存在"
    if y not in data[0]:
        return "错误：指定的值字段名不存在"
    if period <= 0:
        return "错误：period必须是正整数"
    from zhixinpy import func_series

    return func_series.seasonal_decom(arr=data, ds=ds, y=y, period=int(period))


@xlo.func(
    group="知心-序列",
    args={
        "data": "带表头的表格",
        "ds": "【日期轴字段名，字符串，默认空】日期轴字段",
        "y": "【数据轴字段名，字符串，默认是】数据轴字段",
        "periods": "[可选]【周期，数值，默认是12】季节性周期长度，对于年周期为365，月周期为12，",
    },
)
def zs_Prophet(data: xlo.Array(), ds, y, periods=365) -> PDFrame(index=False):
    """使用meta开发的Prophet模型进行时间序列预测，对业务数据预测效果好，尤其是在数据有明显季节性趋势的情况下
    示例
        =zs_Prophet(B2:C59,B2,C2)
    """
    if not (data.shape[0] > 1 and data.shape[1] > 1):
        return "错误：选取的区域必须是表格"
    if not any(isinstance(item, str) for item in data[0]):
        return "错误：选取的区域请包含表格头"
    if ds not in data[0]:
        return "错误：指定的日期字段名不存在"
    if y not in data[0]:
        return "错误：指定的值字段名不存在"
    if periods <= 0:
        return "错误：period必须是正整数"
    from zhixinpy import func_series

    return func_series.prophet(arr=data, ds=ds, y=y, periods=periods)


#################################   func_stat    #########################################


@xlo.func(
    group="知心-统计",
    args={
        "excel_range": "要确定其最小值的单元格范围。",
        "criteria_range1": "要评估其 criterion1 的单元格范围。",
        "criterion1": "要应用于 criteria_range1 的模式或测试。",
        "criteria_range2": "要评估其 criterion2 的单元格范围。",
        "criterion2": "要应用于 criteria_range2 的模式或测试。",
        "more_criteria_ranges_and_criteria": "其他范围及其相关条件（可选）。",
    },
)
@catch_and_log(return_type="na")
def zs_MinIfs(
    excel_range,
    criteria_range1,
    criterion1,
    criteria_range2=None,
    criterion2=None,
    *more_criteria_ranges_and_criteria,
):
    """返回单元格范围中的最小值（按一组条件过滤）。
    示例
        =zs_MinIfs(A1:A3, B1:B3, 1, C1:C3, “A”)
        =zs_MinIfs(D4:E5, F4:G5, “>5”, F6:G7, “<10”)
    """
    from zhixinpy import func_stat

    return func_stat.minIfs(
        excel_range=excel_range,
        criteria_range1=criteria_range1,
        criterion1=criterion1,
        criteria_range2=criteria_range2,
        criterion2=criterion2,
        *more_criteria_ranges_and_criteria,
    )


@xlo.func(
    group="知心-统计",
    args={
        "excel_range": "要确定其最大值的单元格范围。",
        "criteria_range1": "要评估其 criterion1 的单元格范围。",
        "criterion1": "要应用于 criteria_range1 的模式或测试。",
        "criteria_range2": "要评估其 criterion2 的单元格范围。",
        "criterion2": "要应用于 criteria_range2 的模式或测试。",
        "more_criteria_ranges_and_criteria": "其他范围及其相关条件（可选）。",
    },
)
def zs_MaxIfs(
    excel_range,
    criteria_range1,
    criterion1,
    criteria_range2=None,
    criterion2=None,
    *more_criteria_ranges_and_criteria,
):
    """返回单元格范围中的最大值（按一组条件过滤）。
    示例
        =zs_MaxIfs(A1:A3, B1:B3, 1, C1:C3, “A”)
        =zs_MaxIfs(D4:E5, F4:G5, “>5”, F6:G7, “<10”)
    说明
        如果未满足任何条件，则 MAXIFS 会返回 0。
        excel_range 和所有条件范围必须是相同大小。否则，MAXIFS 会返回 #VALUE 错误。
    """
    from zhixinpy import func_stat

    return func_stat.maxIfs(
        excel_range=excel_range,
        criteria_range1=criteria_range1,
        criterion1=criterion1,
        criteria_range2=criteria_range2,
        criterion2=criterion2,
        *more_criteria_ranges_and_criteria,
    )


#################################   func_text    #########################################


@xlo.func(
    group="知心-文本",
    args={"value": "要验证其是否为日期的值。"},
)
@catch_and_log(return_type="na")
def ze_IsDate(value):
    """验证值是否为有效日期格式
    示例：
    =ze_IsDate("2023-10-05") -> TRUE
    =ze_IsDate("20230230") -> FALSE"""
    from zhixinpy import func_text

    return func_text.isDate(value=value)


@xlo.func(
    group="知心-文本",
    args={"value": "要验证其是否为电子邮件地址的值。"},
)
@catch_and_log(return_type="na")
def ze_IsEmail(value):
    """检查输入的值是否为有效的电子邮件地址。
    示例
        =ze_IsEmail("noreply@google.com")
    """
    from zhixinpy import func_text

    return func_text.isEmail(value=value)


@xlo.func(
    group="知心-文本",
    args={
        "text": "输入文本。",
        "regex": "此函数将返回 text 中符合此表达式的第一个子串。",
    },
)
@catch_and_log(return_type="na")
def ze_RegexExtract(text, regex, dilimiter: str = ",") -> str:
    """根据正则表达式提取所有匹配子串，用逗号隔开。
    示例：
        =ze_RegexExtract("电子123表456格", "[0-9]+") -> 123,456
    """
    from zhixinpy import func_text

    return func_text.regexExtract(text=text, regex=regex, dilimiter=dilimiter)


@xlo.func(
    group="知心-文本",
    args={"text": "要用正则表达式测试的文本。", "regex": "用来测试文本的正则表达式。"},
)
@catch_and_log(return_type="na")
def ze_RegexMatch(text: str, regex: str) -> str:
    """判断一段文本是否与正则表达式相匹配。
    示例
        =ze_RegexMatch("电子表格", "S.r")
    """
    from zhixinpy import func_text

    return func_text.regexMatch(text=text, regex=regex)


@xlo.func(
    group="知心-文本",
    args={
        "text": "其中一部分将被替换的文本。",
        "regex": "正则表达式。文本中所有匹配的实例都将被替换。",
        "replacement": "要插入到原有文本中的文本。",
    },
)
@catch_and_log(return_type="na")
def ze_RegexReplace(text, regex, replacement):
    """使用正则表达式将文本字符串中的一部分替换为其他文本字符串。
    示例
        =ze_RegexReplace("电子表格", "S.*d", "床")
    """
    from zhixinpy import func_text

    return func_text.regexReplace(text=text, regex=regex, replacement=replacement)


@xlo.func(
    group="知心-文本",
    args={
        "text": "要拆分的文本。",
        "delimiter": "用于拆分文本的一个或多个字符。",
        "split_each_char": "是否在文本中出现分隔符所含字符的地方进行拆分。",
        "remove_empty_text": "是否要在拆分后移除空白文本信息。",
    },
)
def ze_Split(text, delimiter, split_each_char=True, remove_empty_text=True):
    """将指定字符或字符串两侧的文本拆分，将拆分后的子串存放在行中不同的单元格中。
    示例
        =ze_Split("1,2,3", ",")
        =ze_Split("Alas, poor Yorick"," ")
        =ze_Split(A1, ",")
    """
    from zhixinpy import func_text

    return func_text.split(
        text=text,
        delimiter=delimiter,
        split_each_char=split_each_char,
        remove_empty_text=remove_empty_text,
    )


@xlo.func(
    group="知心-文本",
    args={
        "delimiter": "用于分隔各个文本的字符串或字符。",
        "ignore_empty": "布尔值，是否忽略空白文本。",
        "text1": "任何文本内容，可以是一个字符串或字符串数组。",
        "text2": "其他文本内容。",
    },
)
# @catch_and_log(return_type="na")
def ze_Join(delimiter: str, ignore_empty: bool, text1, *texts):
    """将多个字符串和/或数组中的文本与分隔不同文本的可指定分隔符结合。
    示例
        =ze_Join(" ", TRUE, "hello", "world")
        =ze_Join(", ", FALSE, A1:A5)
    """
    from zhixinpy import func_text

    return func_text.join(
        delimiter=delimiter, ignore_empty=ignore_empty, text1=text1, texts=texts
    )


@xlo.func(
    group="知心-文本",
    args={
        "value": "要验证其是否为网址的值。",
    },
)
def ze_IsURL(value):
    """检查某个值是否为有效网址。
    示例
        =ze_IsURL("https://www.baidu.com")
    """
    from zhixinpy import func_text

    return func_text.isURL(value)


@xlo.func(
    group="知心-文本",
    args={
        "data_range": "输入数据区域（需包含标题行）",
        "rows": "行分组字段（逗号分隔多个字段）",
        "cols": "列分组字段（逗号分隔多个字段）",
        "values": "需要汇总的数值列",
        "aggregation": "聚合方式：sum/count/average/...",
    },
)
@catch_and_log(return_type="na")
def ze_PivotBy(data_range, rows, cols, values, aggregation="sum"):
    """动态生成透视表式汇总，支持百分比占比等高级计算
    示例
        =ze_PivotBy(A1:D100, "区域,产品", "年份", "销售额", "sum")
    提示：将按区域和产品分组行、年份分组列，计算销售额总和，结果动态扩展区域
    语法
        PIVOTBY(data_range, rows, cols, values, aggregation)

        data_range - 原始数据区域（需包含标题行）
        rows - 行分组字段（多字段用逗号分隔）
        cols - 列分组字段（多字段用逗号分隔，可空）
        values - 需要汇总的数值列（需存在于data_range）
        aggregation - 聚合方式（默认sum，支持count/average/max/min等）
    """
    from zhixinpy import func_text

    return func_text.pivot_by(
        data=data_range,
        rows=rows.split(","),
        cols=cols.split(",") if cols else [],
        values=values,
        aggfunc=aggregation,
    )


@xlo.func(
    group="知心-文本",
    args={
        "data_range": "输入数据区域（需包含标题行）",
        "group_cols": "分组字段（逗号分隔多个字段）",
        "agg_cols": "需聚合的数值列及计算方式（格式：列名:聚合方式）",
    },
)
@catch_and_log(return_type="na")
def ze_GroupBy(data_range, group_cols, agg_cols):
    """灵活的分组统计，支持多列聚合计算
    示例
        =ze_GroupBy(A1:D100, "月份,地区", "销售额:sum,客户数:count,单价:average")
    提示：按月+地区分组，计算总销售额、客户数和平均单价，结果动态扩展多列
    语法
        GROUPBY(data_range, group_cols, agg_cols)

        data_range - 原始数据区域（需包含标题行）
        group_cols - 分组字段（多字段用逗号分隔）
        agg_cols - 聚合列定义（格式：列名1:聚合方式1,列名2:聚合方式2）
    """
    from zhixinpy import func_text

    # 解析聚合参数（例如将"销售额:sum"转换为字典）
    agg_dict = {}
    for pair in agg_cols.split(","):
        col, agg = pair.split(":")
        agg_dict[col.strip()] = agg.strip()

    return func_text.group_by(
        data=data_range, groups=group_cols.split(","), aggregations=agg_dict
    )


#################################   ZT 获得高级工具函数    #########################################


def _set_image_size(image, mode, width, height):
    original_width, original_height = image.size
    c = xlo.Caller()
    cell = xlo.Range(c.address(style="a1"))
    if mode == 1:  # 保持图片宽高比，并适配单元格
        if (
            original_width / original_height >= cell.Width / cell.Height
        ):  # 表示图片很宽，那么用单元格的宽作为图片的宽
            pic_width = cell.Width
            pic_height = pic_width * original_height / original_width
        else:
            pic_height = cell.Height
            pic_width = pic_height * original_width / original_height
    elif mode == 2:  # 拉升或压缩填满整个单元格
        pic_width = cell.Width
        pic_height = cell.Height
    elif mode == 3:  # 保持图片大小
        pic_width = original_width
        pic_height = original_height
    else:  # 使用用户指定的大小
        pic_width = width
        pic_height = height

    image = image.resize((int(pic_width), int(pic_height)), Image.LANCZOS)
    xlo.insert_cell_image(
        lambda filename: image.save(filename, format="png"), (pic_width, pic_height)
    )
    return None


@xlo.func(
    group="知心-工具",
    args={
        "words": "【二维码内容，字符串，默认空】需要转成二维码的URL或者内容",
        "mode": "[可选 - 默认值为 4] - 图片的调整大小模式。1：保持宽高比适合单元格。2：拉伸或压缩适合单元格。3：保持原始大小。4：自定义大小。",
        "height": "[可选 - 默认值为 120] - 以像素为单位的图片高度。必须将模式的值设为 4，才能设置自定义高度。",
        "width": "[可选 - 默认值为 120] - 以像素为单位的图片宽度。必须将模式的值设为 4，才能设置自定义宽度。",
        "picture": "[可选]【图片绝对地址，字符串，默认空】如果想把图片与二维码结合，可以把图片的绝对地址写到这个参数",
        "colorized": "[可选]【图片是否彩色，布尔值，默认是】如果指定了图片，可以在这个参数指定二维码是否彩色",
    },
)
def zt_Qrcode(
    words="hello", mode=4, height=120, width=120, picture=None, colorized=True
):
    """生成二维码
    示例
        =zt_Qrcode("https://www.bilibili.com/video/BV16i421e7Ft")
    """
    if mode not in (1, 2, 3, 4):
        return "错误：mode只能在1 2 3 4之中选取"
    from zhixinpy import func_tools

    if mode == 4:
        if height <= 0:
            return "错误：height必须是正整数"
        if width <= 0:
            return "错误：width必须是正整数"
    image = None
    try:
        image = func_tools.qrcode(
            words=words,
            picture=picture,
            colorized=colorized,
        )
    except Exception as e:
        return "二维码生成失败，错误信息为：{}".format(e)
    _set_image_size(image, mode, height, width)
    return "输出二维码"


@xlo.func(
    group="知心-工具",
    args={
        "url": "图片的网址，包含协议部分（例如 http://）。",
        "mode": "[可选 - 默认值为 3] - 图片的调整大小模式。1：保持宽高比适合单元格。2：拉伸或压缩适合单元格。3：保持原始大小。4：自定义大小。",
        "height": "[可选] - 以像素为单位的图片高度。必须将模式的值设为 4，才能设置自定义高度。",
        "width": "[可选] - 以像素为单位的图片宽度。必须将模式的值设为 4，才能设置自定义宽度。",
    },
)
def zt_Image(url, mode=3, height=None, width=None):
    """在单元格中插入一张图片。
    示例
        =zt_Image("https://www.google.com/images/srpr/logo3w.png")
    """
    from zhixinpy import func_tools, func_text

    if not func_text.isURL(url):
        return "错误：url必须是合法URL"
    if mode not in (1, 2, 3, 4):
        return "错误：mode只能在1、2、3、4之中选取"
    if mode == 4:
        if height <= 0:
            return "错误：height必须是正整数"
        if width <= 0:
            return "错误：width必须是正整数"
    image = func_tools.azImage(url=url)
    _set_image_size(image, mode, height, width)
    return "输出图片"


@xlo.func(
    group="知心-工具",
    args={
        "url": "【URL地址，字符串，默认空】视频或者音频的URL地址",
        "media_type": "【下载类型video或者audio，字符串，默认video，可选】video=下载视频 audio=下载音频",
        "proxy": "【代理地址，字符串，默认空，可选】某些视频需要代理才能下载，例如填写 socks5://127.0.0.1:8888",
    },
)
async def zt_Video(url, media_type="video", proxy=None):
    """根据提供的 URL 下载视频或音频文件。
    示例
        =zt_Video("https://www.bilibili.com/video/BV16i421e7Ft/")
        =zt_Video("https://www.bilibili.com/video/BV16i421e7Ft/","audio")
    """
    path = os.environ.get('PYTHONEXECUTABLE', '')
    venv_path = os.path.dirname(os.path.dirname(path))
    if not os.path.exists(
        os.path.join(venv_path, "yt-dlp.exe")
    ):
        yield f"请下载yt-dlp.exe并放到{venv_path}目录下。可从这里下载https://github.com/yt-dlp/yt-dlp/releases/download/2025.05.22/yt-dlp.exe"
        return
    if not os.path.exists(
    	os.path.join(venv_path, "ffmpeg.exe")
    ):
        yield f"请下载ffmpeg.exe并放到{venv_path}目录下。可从这里下载https://www.videohelp.com/download/ffmpeg-7.1.1-full_build.7z"
        return
    from zhixinpy import func_tools

    output_fullpath = os.path.join(xlo.active_workbook().Path, "%(title)s.%(ext)s")
    async for status in func_tools.download_video(
        url, media_type, proxy, output_fullpath
    ):
        yield status


@xlo.func(
    group="知心-工具",
    args={
        "url": "【URL地址，字符串，默认空】需要下载的文件的URL地址",
        "file_name": "【下载后的文件名，字符串，默认取URL最后的文件名，可选】",
    },
)
async def zt_Download(url: str, file_name: str = ""):
    """根据提供的URL下载文件
    示例
        =zt_Download("http://static.cninfo.com.cn/finalpage/2025-04-04/1223006355.PDF")
        =zt_Download("http://static.cninfo.com.cn/finalpage/2025-04-04/1223006355.PDF","安徽省建设总院2024年度年度报告.pdf")
    """

    from zhixinpy import func_tools, func_text

    if not func_text.isURL(url):
        yield "错误：url必须是合法URL"
        return
    if file_name == "":
        file_name = url.split("/")[-1]
    file_name = re.sub(r'[\\/:*?"<>|]', "", file_name)  # 去掉windows不支持的字符
    output_fullpath = os.path.join(xlo.active_workbook().Path, file_name)

    yield "处理中"
    # 随机睡眠1-2秒内，方式避免多线程下载时文件名重复
    await asyncio.sleep(random.randint(1, 2))
    async for status in func_tools.download_file(url=url, full_path=output_fullpath):
        yield status


@xlo.func(
    group="知心-工具",
    args={
        "subject": "【邮件标题，字符串，默认空】邮件的标题",
        "body": "【邮件正文，字符串】邮件的正文",
        "recipients": "【收件人地址列表，选择的区块，默认空】把收件人写到单元格中，选中这一个或多个单元格",
        "filename": r"【附件路径，字符串，默认空，可选】附件在本地的绝对路径，例如 D:\aaa.txt",
    },
)
async def zt_Mail(
    subject: str = "",
    body: str = "",
    recipients: xlo.Array() = np.array([]),
    filenames: xlo.Array() = np.array([]),
):
    """发送邮件，支持批量发送，也支持添加附件。需先点击之心配置-配置文件，填入你的发送地址。
    示例
        =zt_Mail(,"邮件标题","邮件正文",B7:C7)
    参数：
        subject：邮件的标题。
        body：邮件的正文。
        recipients：收件人邮箱地址列表，可以选择多个单元格，每个单元格一个地址。
        filenames：附件在本地的绝对路径。
    """
    config = load_config()
    MAIL_SENDER = config.get("mail", {}).get("MAIL_SENDER", "")
    MAIL_PASSWORD = config.get("mail", {}).get("MAIL_PASSWORD", "")
    MAIL_SMTP_SERVER = config.get("mail", {}).get("MAIL_SMTP_SERVER", "")
    if not MAIL_SENDER:
        raise Exception("点击知心配置-配置文件,填入发送地址。例如：MAIL_SENDER=zhixin_excel@163.com")

    from zhixinpy import func_text, func_tools

    recipients = recipients.flatten().tolist()
    filenames = filenames.flatten().tolist()

    if not func_text.isEmail(MAIL_SENDER):
        yield f"错误：邮箱地址不合法 {MAIL_SENDER}"
        return
    for recipient in recipients:
        if not func_text.isEmail(recipient):
            yield f"错误：邮箱地址不合法 {recipient}"
            return
    for filename in filenames:
        if not os.path.isfile(filename):
            yield f"错误：文件不存在 {filename}"
            return

    async for status in func_tools.mail(
        MAIL_SENDER,
        MAIL_PASSWORD,
        MAIL_SMTP_SERVER,
        subject,
        body,
        recipients,
        filenames,
    ):
        yield status
        if status in ("邮件已发送", "邮件发送出错"):
            return  # 终止生成器


@xlo.func(
    group="知心-工具",
    args={
        "prompt": "提示词。其中{}符号表示第二个参数",
        "input": "[可选 默认空] 第二个参数，辅助用",
        "system_content": "[可选 默认system_content] system这个角色的定义",
        "is_show_reasoning": "[可选 默认False] 是否显示推理过程",
        "temperature": "[可选 默认0.7] 回答的创意性，0-2之间",
    },
)
async def zt_LLM(
    prompt: str,
    input=None,
    system_content: str = "You are a helpful assistant",
    is_show_reasoning: bool = False,
    temperature: float = 0.7,
):
    """调用大语言模型
    示例
        =zt_LLM("用五岁小孩口吻告诉我量子力学")
        =zt_LLM("把{}翻译成英文", "量子力学")
        =zt_LLM("这个{}是邮箱地址则输出Y,否则输出N", "aa@bb.com")
    语法
        其中提示词写得越清晰，甚至有输入输出样例给它，那么结果会更加好。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return
    if input is not None:
        if "{}" in prompt:
            prompt = prompt.replace("{}", f"`{input}`")
        else:
            prompt += input
    from zhixinpy.func_tools import llm

    async for output in llm(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        temperature=temperature,
        prompt=prompt,
        system_content=system_content,
        is_show_reasoning=is_show_reasoning,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "content": "要翻译的内容",
        "target_language": "目标语言",
        "is_show_reasoning": "[可选 默认False] 是否显示推理过程",
        "temperature": "[可选 默认0.7] 回答的创意性，0-2之间",
    },
)
async def zt_LLM_translate(
    content: str,
    target_language: str,
    is_show_reasoning: bool= False,
    temperature: float = 0.7,
):
    """调用大语言模型进行翻译
    示例
        =zt_LLM_translate("苹果", "英语")
    语法
        其中提示词写得越清晰，甚至有输入输出样例给它，那么结果会更加好。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return
    prompt = f"请将`{content}`翻译成`{target_language}`。只要输出翻译结果，不要输出其他任何内容。"

    from zhixinpy.func_tools import llm

    async for output in llm(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        temperature=temperature,
        prompt=prompt,
        system_content="you are a translator",
        is_show_reasoning=is_show_reasoning,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "content": "要翻译的内容",
        "category": "分类",
        "is_show_reasoning": "[可选 默认False] 是否显示推理过程",
        "temperature": "[可选 默认0.7] 回答的创意性，0-2之间",
    },
)
async def zt_LLM_categorize(
    content: str,
    category: str,
    is_show_reasoning: bool= False,
    temperature: float = 0.7,
):
    """调用大语言模型，将内容进行分类，分类可用逗号隔开
    示例
        =zt_LLM_categorize("今天天气不错", "乐观，悲观，中性")
    语法
        其中提示词写得越清晰，甚至有输入输出样例给它，那么结果会更加好。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return
    prompt = f"请将`{content}`分类为以下类别：`{category}`。类别用全角或者半角逗号隔开，务必严格分类，务必只返回其中一个类别，不要返回其他内容。"

    from zhixinpy.func_tools import llm

    async for output in llm(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        temperature=temperature,
        prompt=prompt,
        system_content="you are a classifier",
        is_show_reasoning=is_show_reasoning,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "content": "要提取的原始内容",
        "extract_type": "提取内容，例如邮箱/电话/网址/姓名",
        "system_content": "[可选 默认system_content] system这个角色的定义",
        "temperature": "[可选 默认0.7] 回答的创意性，0-2之间",
    },
)
async def zt_LLM_extract(
    content: str,
    # 要从中提取的内容 可以填 email 电话 qq 微信号 网址 姓名 地址 公司 职位 行业 部门 描述 介绍 理由 要求 条件 限制 目标 作用 效果 结果 输出 内容 格式 长度 语气 风格
    extract_type: str,
    is_show_reasoning: bool = False,
    temperature: float = 0.7,
) -> xlo.Array:
    """利用利用少量示例，让大语言模型更懂你的需求。支持多列
    示例
        =zLLMEx(A1:B3, C1:C10)
    语法
        其中提示词写得越清晰，甚至有输入输出样例给它，那么结果会更加好。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return
    # 构建系统化的prompt
    task_instruction = f"""请严格按照以下要求执行任务：
1. 从`{content}`中提取`{extract_type}`
2. 举例来说从`你好abc@abc.com哈哈，cc@bbc.com.cn`中提取`邮箱`则输出`abc@abc.com###cc@bbc.com.cn`"""
    # 添加格式要求
    task_instruction += f"""3. 输出格式要求：
   - 不要添加任何编号、序号或解释性文字
   - 邮箱只含数字字母字符等，不包含中文
4. 现在请开始转换，只需返回符合要求的输出字符串"""

    from zhixinpy.func_tools import llmEx

    async for output in llmEx(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        prompt=task_instruction,
        system_content='you are an extractor',
        is_show_reasoning=is_show_reasoning,
        temperature=temperature,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "content": "要改写的内容",
        "tone": "语气",
        "format": "输出格式",
        "writingStyle": "写作风格",
        "length": "长度",
        "is_show_reasoning": "[可选 默认False] 是否显示推理过程",
        "temperature": "[可选 默认0.7] 回答的创意性，0-2之间",
    },
)
async def zt_LLM_rewrite(
    content: str,
    tone: str,
    format: str = '普通文本',
    writingStyle: str = '专业',
    length: str = '20',
    is_show_reasoning: bool= False,
    temperature: float = 0.7,
):
    """调用大语言模型，将内容进行分类，分类可用逗号隔开
    示例
        =zt_LLM_categorize("今天天气不错", "乐观，悲观，中性")
    语法
        其中提示词写得越清晰，甚至有输入输出样例给它，那么结果会更加好。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return
    prompt = f"""请严格按照以下要求执行任务：
1. 你是一个内容转换器，需要根据提供的示例模式进行转换
2. 转换内容：`{content}`
3. 转换要求：
    - 长度要求：{length}个单位
    - 语气：{tone}
    - 写作风格：{writingStyle}
    - 输出格式：{format}
4. 只要输出转换后的内容，不要输出解释之类的别的内容。
5.用原语言，例如原来时中文则输出中文，英文则输出英文。
    """

    from zhixinpy.func_tools import llm

    async for output in llm(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        temperature=temperature,
        prompt=prompt,
        system_content="you are a content rewrite assistant",
        is_show_reasoning=is_show_reasoning,
    ):
        yield output



@xlo.func(
    group="知心-工具",
    args={
        "examples": "包含两列数据，第一列是输入，第二列是输出",
        "inputs": "包含一列数据，表示输入",
        "prompt": "[可选 默认空] 额外的提示词",
        "temperature": "[可选 默认0.7] 回答的创意性，0-2之间",
    },
)
async def zt_LLMEx(
    examples: xlo.Array(),
    inputs: xlo.Array(),
    is_show_reasoning: bool = False,
    temperature: float = 0.7,
) -> xlo.Array:
    """利用利用少量示例，让大语言模型更懂你的需求。支持多列
    示例
        =zt_LLMEx(A1:B3, C1:C10)
    语法
        其中提示词写得越清晰，甚至有输入输出样例给它，那么结果会更加好。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return
    # 构建系统化的prompt
    task_instruction = """请严格按照以下要求执行任务：
1. 你是一个输入-输出转换器，需要根据提供的示例模式将输入转换为输出
2. 转换规则如下：\n"""

    # 添加示例说明
    example_pairs = []
    for row in examples:
        example_pairs.append(f"数据`{row[0]}`对应数据`{row[1]}`")
    task_instruction += "\n".join(example_pairs) + "\n\n"

    # 添加格式要求
    task_instruction += f"""3. 输出格式要求：
   - 输入是`{"###".join(x[0] for x in examples)}`则输出是`{"###".join(x[1] for x in examples)}`
   - 你必须给出输入`{"###".join(inputs.flatten())}`对应的输出
   - 不要添加任何编号、序号或解释性文字
   - 确保输出数量严格等于输入数量
   
4. 现在请开始转换，只需返回符合要求的输出字符串"""

    from zhixinpy.func_tools import llmEx

    async for output in llmEx(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        prompt=task_instruction,
        system_content='You are a helpful assistant',
        is_show_reasoning=is_show_reasoning,
        temperature=temperature,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "input_data": "一列示例数据，用于确定生成的类型",
        "num": "[可选 默认10] 需要生成的数据数量",
        "temperature": "[可选 默认0.7] 创意性，0-2之间",
    },
)
async def zt_LLMGen(
    input_data: xlo.Array(),
    num: int = 10,
    is_show_reasoning: bool = False,
    temperature: float = 0.7,
) -> xlo.Array:
    """根据示例数据生成指定数量的同类测试数据
    示例
        =zLLMGen(A1:A3 , 2) 输出浙江、上海等同类数据
    语法
        通过分析输入数据的模式，生成符合该模式的新数据。
        请务必确保在知心-大语言模型中，已配置正确的API地址以及APIKEY。
    """
    config = load_config()
    llm_url = config.get("llm", {}).get("LLM_URL", "")
    llm_key = config.get("llm", {}).get("LLM_KEY", "")
    llm_model_name = config.get("llm", {}).get("LLM_MODEL_NAME", "")

    # 检查配置是否正确
    if not llm_model_name or len(llm_model_name) <= 1:
        yield "请在知心配置中设置正确的模型名称"
        return
    if not llm_url:
        yield "请在知心配置中设置正确的API地址"
        return
    if not llm_key:
        yield "请在知心配置中设置正确的API密钥"
        return

    examples = input_data.flatten()
    if len(examples) <= 0:
        yield "错误：示例数据不能为空"
        return

    examples_str = "###".join(examples)
    prompt = f"""你是一个测试数据生成器。请严格按照以下要求执行任务：
1. 分析以下示例数据的模式和类型,多个以`###`隔开：{examples_str}
2. 生成{num}个完全相同类型的新数据
3. 输出格式要求：
   - 每个数据之间必须用`###`分隔
   - 不要添加任何编号、序号
   - 不要包含任何解释性文字
   - 生成的数据不要与示例数据重复
   - 确保生成的数据数量严格等于{num}个
4. 示例输出格式：数据1###数据2###数据3（当num=3时）

请开始生成数据，只需返回符合要求的数据字符串，不要包含其他任何内容。"""

    from zhixinpy.func_tools import llmGen

    async for output in llmGen(
        api_key=llm_key,
        base_url=llm_url,
        model=llm_model_name,
        prompt=prompt,
        input_data=input_data,
        num=num,
        system_content='you are a data generator',
        is_show_reasoning=is_show_reasoning,
        temperature=temperature,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "xpath": "【默认空】待爬的列表中第五个元素对应的xpath",
        "sub_xpaths": "【默认空】需要具体提取的xpath表达式",
        "is_cumulative": "【默认False】是否保留累计下来不一样的，还是说只要同步页面",
        "is_reload": "【默认False】是否每次循环检测页面， 需要刷新页面",
        "browser_url": "【连接到Chrome，默认http://localhost:9222，可选】",
    },
)
async def zt_Crawler(
    xpath="/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[5]/div",
    sub_xpaths: xlo.Array() = np.array([]),
    is_cumulative=False,
    is_reload=False,
    browser_url="http://localhost:9222",
) -> xlo.Array:
    """爬虫
    示例
        =zt_Crawler("/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[5]/div")
        =zt_Crawler("/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[5]/div",False, "http://localhost:9222")
    步骤:
        1 关闭所有chrome程序
        2 找到chrome的路径，在cmd中加启动参数，例如 C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222
        3 访问chrome://inspect -> 确保Discover network targets勾选上 -> 点Configure -> 增加localhost:9222 -> 确保Enable port forwarding勾选上
        4 打开新标签页浏览你想爬虫的网站，例如https://www.cls.cn/telegraph
        5 通过F12找到页面上爬虫列表中要爬的要素，右键 -> Copy -> Copy Full Xpath
        6 至此得到了Xpath，保持待爬标签页活跃，调用zt_Crawlerr开始爬虫
    """
    sub_xpaths = sub_xpaths.flatten().tolist()

    from zhixinpy.func_tools import crawler

    async for output in crawler(
        main_xpath=xpath,
        element_xpaths=sub_xpaths,
        is_cumulative=is_cumulative,
        is_reload=is_reload,
        browser_url=browser_url,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "xpath": "【默认空】待爬的列表中要爬的元素对应的xpath",
        "sub_xpaths": "【默认空】需要具体提取的xpath表达式",
        "next_button_xpath": "【下一页按钮对应的xpath，默认空】下一页按钮的xpath",
        "browser_url": "【连接到Chrome，默认http://localhost:9222，可选】",
    },
)
async def zt_CrawlerAll(
    xpath="/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[5]/div",
    sub_xpaths: xlo.Array() = np.array([]),
    next_button_xpath="/html/body/div[3]/div[1]/div/div[1]/div[2]/span[3]/a",
    sleep_time=1.0,
    browser_url="http://localhost:9222",
) -> xlo.Array:
    """爬虫，支持自动点击下一页。按ESC可停止自动翻页
    示例
        =zt_CrawlerAll("/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[5]/div", "/html/body/div[3]/div[1]/div/div[1]/div[2]/span[3]/a")
        =zt_CrawlerAll("/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[5]/div","/html/body/div[3]/div[1]/div/div[1]/div[2]/span[3]/a", "http://localhost:9222")
    步骤:
        1 关闭所有chrome程序
        2 找到chrome的路径，在cmd中加启动参数，例如 C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222
        3 访问chrome://inspect -> 确保Discover network targets勾选上 -> 点Configure -> 增加localhost:9222 -> 确保Enable port forwarding勾选上
        4 打开新标签页浏览你想爬虫的网站，例如https://www.cls.cn/telegraph
        5 通过F12找到页面上爬虫列表中第五个要素，右键 -> Copy -> Copy Full Xpath
        6 至此得到了Xpath，保持待爬标签页活跃，调用zCrawler开始爬虫
    """
    sub_xpaths = sub_xpaths.flatten().tolist()

    from zhixinpy.func_tools import crawlerAll

    async for output in crawlerAll(
        main_xpath=xpath,
        element_xpaths=sub_xpaths,
        next_button_xpath=next_button_xpath,
        sleep_time=sleep_time,
        browser_url=browser_url,
    ):
        yield output


@xlo.func(
    group="知心-工具",
    args={
        "user_privkey": "用户私钥",
    },
)
def zt_GenPubKey(user_privkey: str) -> str:
    """使用自己记得住的口令生成公钥，生成的公钥在%appdata%/xlOil/pubkey.txt
    示例
        =zGenPubKey("myPrivateKey")
    """
    from zhixinpy import func_tools

    # 结果除了返回给用户，也写到 pub_key_path = os.path.join(os.environ['appdata'], 'xlOil', 'pubkey.txt')
    pub_key = func_tools.gen_pubkey(user_privkey)
    pub_key_path = os.path.join(os.environ["appdata"], "xlOil", "pubkey.txt")
    if os.path.exists(pub_key_path):
        return f"公钥已存在，手工删除后才可重新创建{pub_key_path}"
    with open(pub_key_path, "w") as f:
        f.write(pub_key)
    return f"已生成公钥至{pub_key_path}"


@xlo.func(
    group="知心-工具",
    args={
        "plaintext": "明文",
    },
)
def zt_Encrypt(plaintext) -> str:
    """使用公钥加密明文，公钥需要先用函数=zGenPubKey()生成
    示例
        =zEncrypt("我需要加密的内容")
    """
    from zhixinpy import func_tools

    pub_key_path = os.path.join(os.environ["appdata"], "xlOil", "pubkey.txt")
    if not os.path.exists(pub_key_path):
        return "请先用函数=zGenPubKey()生成公钥"
    with open(pub_key_path, "r") as f:
        public_key = f.read()
    return func_tools.encrypt(public_key, plaintext)


@xlo.func(
    group="知心-工具",
    args={
        "private_key_str": "私钥",
        "encrypted_data": "密文",
    },
)
def zt_Decrypt(private_key_str, encrypted_data) -> str:
    """使用私钥解密密文
    示例
        =zDecrypt("myPrivateKey", "加密后的内容")
    """
    from zhixinpy import func_tools

    return func_tools.decrypt(private_key_str, encrypted_data)


@xlo.func(
    group="知心-工具",
    args={
        "text": "文字转语音中的文字",
    },
)
async def zt_tts(text: str):
    """利用Windows内置接口进行，文字转语音
    示例
        =zt_tts("你好，hello world")
    """
    # 检查text是否为空或转换为字符串后长度为0
    if text is None or len(str(text).strip()) == 0:
        return
    from zhixinpy.func_tools import tts

    async for status in tts(text):
        yield status


@xlo.func(
    group="知心-工具",
    args={
        "title": "通知标题",
        "content": "通知内容",
        "delay_seconds": "几秒后发送通知",
    },
)
def zt_Notice(title: str = "", content: str = "", delay_seconds: int = 3) -> str:
    """发送通知
    示例
        =zt_Notice("通知的标题", "通知的内容", 10)  # 10秒后发送桌面通知
    """
    from zhixinpy import func_tools

    func_tools.win_notification(
        title=title, content=content, delay_seconds=delay_seconds
    )
    return "已设置通知"


@xlo.func(
    group="知心-工具",
    args={
        "src": "原文件地址，绝对路径或者相对路径，例如 input.mp3",
        "dest": "目标文件地址，例如 output.mp4",
    },
)
async def zt_Convert_Media(src: str, dest: str):
    """多媒体文件格式转化
    示例:
        =zt_Convert_Media('input.m4a','output.mp3')
    备注:
        支持视频格式：['.mp4', '.mkv', '.mov', '.avi', '.webm']
        支持音频格式：['.mp3', '.wav', '.m4a', '.flac', '.aac']
        他们之间的转换，如果是音频转视频，则视频为黑屏。
    """
    path = os.environ.get('PYTHONEXECUTABLE', '')
    venv_path = os.path.dirname(os.path.dirname(path))
    if not os.path.exists(
        os.path.join(venv_path, "ffmpeg.exe")
    ):
        yield f"请下载ffmpeg.exe并放到{venv_path}目录下"
        return
    SUBFIX_LIST = [
        "mp4",
        "mkv",
        "mov",
        "avi",
        "webm",
        "mp3",
        "wav",
        "m4a",
        "flac",
        "aac",
    ]
    if src.split(".")[-1] not in SUBFIX_LIST:
        raise Exception(f'原文件仅支持这些格式：{",".join(SUBFIX_LIST)}')

    if dest.split(".")[-1] not in SUBFIX_LIST:
        raise Exception(f'目标文件仅支持这些格式：{",".join(SUBFIX_LIST)}')

    if not os.path.isabs(src):
        src = os.path.join(xlo.active_workbook().Path, src)

    if not os.path.isabs(dest):
        dest = os.path.join(xlo.active_workbook().Path, dest)

    from zhixinpy import func_tools

    cmd = func_tools.convert_media_cmd(src=src, dest=dest)
    python_path = os.environ.get("PYTHONPATH", "").split(os.pathsep)[0]
    bin_path = os.path.join(python_path, "bin")

    try:
        # 创建异步子进程
        process = await asyncio.create_subprocess_exec(
            *cmd,  #   将命令和参数展开传入
            cwd=bin_path,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        i = 0
        while process.returncode is None:
            yield CONVERTING_ANIMATION[i]
            i = (i + 1) % len(CONVERTING_ANIMATION)  # 循环更新动画索引
            await asyncio.sleep(1)

        # 检查子进程是否成功
        if process.returncode == 0:
            yield "已下载"
        else:
            error_output = await process.stderr.read()
            yield f"执行出错: {error_output.decode()}"

    except Exception as e:
        yield f"执行命令出错：{e}"


@xlo.func(
    group="知心-工具",
    args={
        "idcard": "身份证号",
    },
)
def zt_idcard_info(idcard: str):
    """从身份证号提取地区、生日、性别、校验等等
    示例:
        =zt_idcard_info('11010119900307001X')
    """
    from zhixinpy import func_tools

    res = func_tools.idcard_info(idcard)
    if res['code'] != 0:
        return res['msg']
    excel_birth_date = dt.datetime.strptime(res['birth'], "%Y%m%d").strftime("%Y/%m/%d")
    ret = [[res['province'], res['city'], res['county'], excel_birth_date, res['gender']]]
    return ret


@xlo.func(
    group="知心-工具",
    args={
        "bank_card": "银行卡号",
    },
)
def zt_validate_bank_card(bank_card: str):
    """校验银行卡号
    示例:
        =zt_validate_bank_card('6222021000000000000')
    """
    from zhixinpy import func_tools

    is_valid, msg = func_tools.validate_bank_card(bank_card)
    if is_valid:
        return "校验成功"
    else:
        return f"校验失败：{msg}"
    

#################################   高级图表    #########################################


def format_kwargs(kwargs):
    """
    值为空的去掉
    值中有{}的，尝试转成dict数据
    """
    kwargs = {
        str(key).strip(): value.strip() if type(value) == str else value
        for key, value in kwargs.items()
        if str(key).strip() != ""
    }
    for key, value in kwargs.items():
        if isinstance(value, str) and "{" in value and "}" in value:
            try:
                kwargs[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
    return kwargs


@xlo.func(
    group="知心-图表",
    args={
        "nodes": "【带表头的表格，选择区域】含节点名称、节点类型",
        "connections": "【带表头的表格，选择区域】含源节点、目标节点、连接值、同比",
        "title": "桑基图标题，默认空",
    },
)
def zc_Sankey_income(nodes: xlo.Array(), connections: xlo.Array(), title=""):
    """专门用于可视化财报利润表
    示例
        =zc_Sankey_income(区域1, 区域2)
        参数1举例：
        节点名  节点类型
        北美     收入
        东亚     收入
        研发     费用
        营销     费用
        零售额  利润

        参数2举例：
        源节点 目标节点 值   同比
        北美   零售额   20  9.8%
        东亚   零售额   30  9.8%
        总收入  研发    25  9.8%
        总收入  利息     5  9.8%

    简介
        通过节点定义、节点链接定义，画桑基图
    """
    if nodes.shape[1] < 2:
        return "错误：必须要包含2列。节点列，类型列"
    if connections.shape[1] < 3:
        return "错误：必须包含3列，源节点名，目的节点名，值"
    from zhixinpy import func_chart

    NODE_COLORS = ["rgb(44, 160, 44)", "rgb(204, 0, 0)", "rgb(102, 102, 102)"]
    CONNECTION_COLORS = ["rgb(153,205,153)", "rgb(225,133,133)", "rgb(179,179,179)"]
    nodes = load_to_dataframe(nodes)
    nodes.columns = ["nodeName", "nodeType"]
    nodes["colorindex"] = nodes.groupby("nodeType").ngroup() % 3
    nodes["color"] = nodes["colorindex"].apply(lambda x: NODE_COLORS[x])
    nodes["rownum"] = range(len(nodes))

    connections = load_to_dataframe(connections)
    connections.columns = ["source", "destination", "value", "yoy"]
    for src in connections["source"].values:
        if src not in nodes["nodeName"].values:
            return f"错误：源节点{src}不在参数1定义的节点列表里"
    for dest in connections["destination"].values:
        if dest not in nodes["nodeName"].values:
            return f"错误：目的节点{dest}不在参数1定义的节点列表里"

    # connections特殊处理，如果source和destination一样，说明是桑基图的中间节点，需要提取数据，并过滤它
    # 它的value 和 yoy放到dict中 middle_node_data = {'中间节点名称': {'value': value, 'yoy': yoy}}
    middle_node_data = {}
    for src, dest, value, yoy in zip(
        connections["source"].values,
        connections["destination"].values,
        connections["value"].values,
        connections["yoy"].values,
    ):
        if src == dest:
            middle_node_data[src] = {"value": value, "yoy": yoy}

    # 中间节点必须有数据
    for i, row in nodes.iterrows():
        if (
            row["nodeName"] not in connections["source"].values
            and row["nodeName"] not in connections["destination"].values
        ):
            continue
        if (
            row["nodeName"] in connections["source"].values
            and row["nodeName"] in connections["destination"].values
        ):
            # 中间节点
            if row["nodeName"] not in middle_node_data:
                return f"错误：中间节点{row['nodeName']}没有数据"

    connections = connections[(connections["source"] != connections["destination"])]

    connections = connections[
        (connections["value"] > 0.05) | (connections["value"] < -0.05)
    ]
    connections = connections.merge(
        nodes, left_on="destination", right_on="nodeName", how="left"
    )
    connections = connections.merge(
        nodes[["nodeName", "rownum"]].rename(
            columns={"nodeName": "source", "rownum": "sourceRownum"}
        ),
        on="source",
        how="left",
    )
    connections["color"] = connections["colorindex"].apply(
        lambda x: CONNECTION_COLORS[x]
    )

    # 计算每个节点的描述
    nodes["label"] = ""
    for i, row in nodes.iterrows():
        if (
            row["nodeName"] not in connections["source"].values
            and row["nodeName"] not in connections["destination"].values
        ):
            continue
        elif (
            row["nodeName"] in connections["source"].values
            and row["nodeName"] not in connections["destination"].values
        ):  # 出发节点
            the_value = np.round(
                np.sum(connections[connections["source"] == row["nodeName"]]["value"]),
                2,
            )
            the_yoy = connections[connections["source"] == row["nodeName"]]["yoy"].iloc[
                0
            ]
            the_yoy_str = (
                f"<span style='color: green;'>{the_yoy:.2%}</span>"
                if the_yoy < 0
                else f"<span style='color: red;'>{the_yoy:.2%}</span>"
            )
            nodes.at[i, "label"] = f"{row['nodeName']}<br>{the_value}亿({the_yoy_str})"
        elif (
            row["nodeName"] not in connections["source"].values
            and row["nodeName"] in connections["destination"].values
        ):  # 结束节点
            if row["nodeName"] == "净利润":  # 净利润这个特殊处理，因为它有其他利润以及营业利润流转到它
                the_row = connections[
                    (connections["destination"] == "净利润")
                    & (connections["source"] == "营业利润")
                ].iloc[0]
            else:
                the_row = connections[
                    connections["destination"] == row["nodeName"]
                ].iloc[0]
            the_value = the_row["value"]
            the_yoy = the_row["yoy"]
            the_yoy_str = (
                f"<span style='color: green;'>{the_yoy:.2%}</span>"
                if the_yoy < 0
                else f"<span style='color: red;'>{the_yoy:.2%}</span>"
            )
            nodes.at[i, "label"] = f"{row['nodeName']}<br>{the_value}亿({the_yoy_str})"
        else:  # 中间节点
            the_value = middle_node_data.get(row["nodeName"]).get("value")
            the_yoy = middle_node_data.get(row["nodeName"]).get("yoy")
            the_yoy_str = (
                f"<span style='color: green;'>{the_yoy:.2%}</span>"
                if the_yoy < 0
                else f"<span style='color: red;'>{the_yoy:.2%}</span>"
            )
            nodes.at[i, "label"] = f"{row['nodeName']}<br>{the_value}亿({the_yoy_str})"
    connections["value"] = np.abs(connections["value"])  # 节点描述之后，就可以给连接绝对值了

    return func_chart.sankey_income(nodes=nodes, connections=connections, title=title)


def _df_type_converter(data_frame, kwargs):
    if "animation_frame" in kwargs.keys():
        data_frame = data_frame.sort_values(by=kwargs.get("animation_frame"))
    for attr in (
        "thickness",
        "value",
        "valueminus",
        "width",
        "start",
        "stop",
        "fgopacity",
        "size",
        "solidity",
        "backoff",
        "smoothing",
        "cmax",
        "cmid",
        "cmin",
        "maxdisplayed",
        "opacity",
        "sizemin",
        "sizeref",
        "standoff",
        "maxpoints",
    ):
        col = kwargs.get(attr)
        if col:
            data_frame[col] = pd.to_numeric(data_frame[col], errors="coerce")
    date_columns = kwargs.get("date_columns", "")
    for col in date_columns.split(","):
        if col in data_frame.columns:
            data_frame[col] = data_frame[col].apply(
                lambda x: date_str_to_dt(x) if pd.notnull(x) else x
            )
    # kwargs若含有date_columns则要去掉，因为它不是标准的plotly key
    if "date_columns" in kwargs.keys():
        kwargs.pop("date_columns")
    save_html = False  # 是否要保存为html
    if "html" in kwargs.keys() and kwargs["html"]:
        kwargs.pop("html")
        save_html = True
    return data_frame, kwargs, save_html


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，默认空】X轴字段名",
        "y": "【字段名，默认空】Y轴字段名",
        "hover_data": "【字段名，默认空】需要提示出来的字段名，若有多个字段，可用逗号隔开",
        "size": "【字段名，默认空】散点气泡大小字段名",
        "color": "【字段名，默认空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Scatter(
    data_frame: xlo.Array(),
    x: str,
    y: str,
    hover_data: str = "",
    size: str = "",
    color: str = "",
    **kwargs,
):
    """散点图
    =zc_Scatter()
    简介
        画散点图，每一行数据代表一个观测值
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y})
    if hover_data:
        if "," in hover_data:
            hover_data = hover_data.split(",")
        elif "，" in hover_data:
            hover_data = hover_data.split("，")
        else:
            hover_data = [hover_data]
        kwargs.update({"hover_data": hover_data})
    if size:
        kwargs.update({"size": size})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.scatter(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，默认空】X轴字段名",
        "y": "【字段名，默认空】Y轴字段名",
        "z": "【字段名，默认空】Z轴字段名",
        "hover_data": "【字段名，默认空】需要提示出来的字段名，若有多个字段，可用逗号隔开",
        "size": "【字段名，默认空】散点气泡大小字段名",
        "color": "【字段名，默认空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Scatter3d(
    data_frame: xlo.Array(),
    x: str,
    y: str,
    z: str,
    hover_data: str = "",
    size: str = "",
    color: str = "",
    **kwargs,
):
    """
    =zc_Scatter3d()
    简介
        画三维散点图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y, "z": z})
    if hover_data:
        if "," in hover_data:
            hover_data = hover_data.split(",")
        elif "，" in hover_data:
            hover_data = hover_data.split("，")
        else:
            hover_data = [hover_data]
        kwargs.update({"hover_data": hover_data})
    if size:
        kwargs.update({"size": size})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.scatter_3d(
        data_frame=data_frame, save_html=save_html, kwargs=kwargs
    )


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "lon": "【字段名，则空】经度字段名",
        "lat": "【字段名，则空】纬度字段名",
        "color": "【字段名，则空】颜色字段名",
        "size": "【字段名，则空】散点气泡大小字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_ScatterMap(
    data_frame: xlo.Array(),
    lon: str,
    lat: str,
    color: str = "",
    size: str = "",
    **kwargs,
):
    """散点地图
    =zc_ScatterMap()
    简介
        散点地图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"lat": lat, "lon": lon})
    if color:
        kwargs.update({"color": color})
    if size:
        kwargs.update({"size": size})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.scatter_map(
        data_frame=data_frame, save_html=save_html, kwargs=kwargs
    )


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "y": "【字段名，则空】Y轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Line(data_frame: xlo.Array(), x: str, y: str, color: str = "", **kwargs):
    """折线图绘制函数
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.line(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "y": "【字段名，则空】Y轴字段名",
        "z": "【字段名，则空】Z轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Line3d(
    data_frame: xlo.Array(), x: str, y: str, z: str, color: str = "", **kwargs
):
    """
    =zc_Line3d()
    简介
        三维折线图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y, "z": z})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.line_3d(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "lon": "【字段名，则空】经度字段名",
        "lat": "【字段名，则空】纬度字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_LineMap(data_frame: xlo.Array(), lon: str, lat: str, color: str = "", **kwargs):
    """折线地图
    =zc_LineMap()
    简介
        折线图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"lat": lat, "lon": lon})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.line_map(
        data_frame=data_frame, save_html=save_html, kwargs=kwargs
    )


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "y": "【字段名，则空】Y轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "line_group": "【字段名，则空】分组字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Area(
    data_frame: xlo.Array(),
    x: str,
    y: str,
    color: str = "",
    line_group: str = "",
    **kwargs,
):
    """
    =zc_Area()
    简介
        堆积面积图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y})
    if color:
        kwargs.update({"color": color})
    if line_group:
        kwargs.update({"line_group": line_group})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.area(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "y": "【字段名，则空】Y轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Bar(data_frame: xlo.Array(), x: str, y: str, color: str = "", **kwargs):
    """
    =zc_Bar()
    简介
        条形图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.bar(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "y": "【字段名，则空】Y轴字段名",
        "x": "【字段名，则空】X轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Violin(data_frame: xlo.Array(), y: str, x: str = "", color: str = "", **kwargs):
    """
    =zc_Violin()
    简介
        小提琴图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"y": y})
    if x:
        kwargs.update({"x": x})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.violin(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "y": "【字段名，则空】Y轴字段名",
        "x": "【字段名，则空】X轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Box(data_frame: xlo.Array(), y: str, x: str = "", color: str = "", **kwargs):
    """
    =zc_Box()
    简介
        箱形图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"y": y})
    if x:
        kwargs.update({"x": x})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.box(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "y": "【字段名，则空】Y轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Ecdf(data_frame: xlo.Array(), x: str, y: str = "", color: str = "", **kwargs):
    """
    =zc_Ecdf()
    简介
        经验累积分布函数图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    if "," in x:
        kwargs.update({"x": x.split(",")})
    elif "，" in x:
        kwargs.update({"x": x.split("，")})
    else:
        kwargs.update({"x": x})
    if y:
        kwargs.update({"y": y})
    if color:
        kwargs.update({"color": color})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.ecdf(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "y": "【字段名，则空】Y轴字段名",
        "color": "【字段名，则空】颜色字段名",
        "facet_col": "【字段名，则空】分面字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Strip(
    data_frame: xlo.Array(),
    x: str,
    y: str,
    color: str = "",
    facet_col: str = "",
    **kwargs,
):
    """
    =zc_Strip()
    简介
        条形散点图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "y": y})
    if color:
        kwargs.update({"color": color})
    if facet_col:
        kwargs.update({"facet_col": facet_col})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.strip(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "x": "【字段名，则空】X轴字段名",
        "nbins": "【字段名，则空】bins",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Histogram(data_frame: xlo.Array(), x: str, nbins: int = 10, **kwargs):
    """
    =zc_Histogram()
    简介
        直方图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"x": x, "nbins": nbins})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.histogram(
        data_frame=data_frame, save_html=save_html, kwargs=kwargs
    )


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "names": "【字段名，则空】名称字段名",
        "values": "【字段名，则空】数值字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Pie(data_frame: xlo.Array(), names: str = "", values: str ="", **kwargs):
    """
    =zc_Pie()
    简介
        饼图
    """
    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    kwargs.update({"values": values})
    if names:
        kwargs.update({"names": names})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.pie(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "path": "【字段名，则空】路径字段名",
        "values": "【字段名，则空】数值字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Treemap(
    data_frame: xlo.Array(), path: str, values: str, color: str = "", **kwargs
):
    """
    =zc_Treemap()
    简介
        树状图
    """
    import plotly.express as px

    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    if "," in path:
        path = [px.Constant("all")] + path.split(",")
    elif "，" in path:
        path = [px.Constant("all")] + path.split("，")
    else:
        path = [px.Constant("all"), path]
    kwargs.update({"path": path, "values": values})
    if color:
        kwargs.update({"color": color, "color_continuous_scale": "RdBu"})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.treemap(data_frame=data_frame, save_html=save_html, kwargs=kwargs)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格",
        "path": "【字段名，则空】路径字段名",
        "values": "【字段名，则空】数值字段名",
        "color": "【字段名，则空】颜色字段名",
        "kwargs": "【函数参数列表及参数值，选择区域】",
    },
)
def zc_Sunburst(
    data_frame: xlo.Array(), path: str, values: str, color: str = "", **kwargs
):
    """
    =zc_Sunburst()
    简介
        日晕图
    """
    import plotly.express as px

    if data_frame.shape[1] < 2:
        return "错误：必须带有表格名"
    data_frame = load_to_dataframe(data_frame)
    if type(kwargs) != dict:
        return "错误：参数类型错误，需要字典类型"
    if "," in path:
        path = [px.Constant("all")] + path.split(",")
    elif "，" in path:
        path = [px.Constant("all")] + path.split("，")
    else:
        path = [px.Constant("all"), path]
    kwargs.update({"path": path, "values": values})
    if color:
        kwargs.update({"color": color, "color_continuous_scale": "RdBu"})
    kwargs = format_kwargs(kwargs)
    data_frame, kwargs, save_html = _df_type_converter(data_frame, kwargs)
    from zhixinpy import func_chart

    return func_chart.sunburst(
        data_frame=data_frame, save_html=save_html, kwargs=kwargs
    )


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "word_column": "【词语字段名】",
        "weight_column": "【权重/频次字段名】",
    },
)
def zc_WordCloud(
    data_frame: xlo.Array(),
    word_column: str = "词语",
    weight_column: str = "权重",
    title: str = "词云图",
):
    """根据输入的表格数据生成词云图。
    =zc_WordCloud()
    示例
        zc_WordCloud(data_frame=data_frame, word_column="词语", weight_column="权重", title="词云图")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")

    return func_chart.wordcloud(
        df=df, word_column=word_column, weight_column=weight_column, title=title
    )


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "source": "【源节点字段名】",
        "target": "【目标节点字段名】",
        "value": "【权重节点字段名】",
        "color": "【颜色节点字段名】",
        "title": "【标题】",
    },
)
def zc_sankey(
    data_frame: xlo.Array(),
    source: str,
    target: str,
    value: str,
    color: str,
    title: str = "",
):
    """根据输入的表格数据生成桑基图。
    =zc_sankey()
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")

    return func_chart.sankey(df, source, target, value, color, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "city_column": "【城市字段名】",
        "weight_column": "【权重字段名】",
        "maptype": "【国内区域地图名，默认中国】可填 广东 上海 广州 等",
        "title": "【标题】",
    },
)
def zc_Geo(
    data_frame: xlo.Array(),
    city_column: str,
    weight_column: str,
    maptype: str = "中国",
    title: str = "地图",
    color_series: str = '蓝色',
):
    """根据输入的表格数据生成地图数据。
    示例
        =zc_Geo(data_frame=data_frame, city_column="城市", weight_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    if maptype in ["china", "china-cities"]:  # 标准化省级城市名称
        df[city_column] = df[city_column].apply(standardize_province_name)
    weight_column = date2str(weight_column)

    return func_chart.geo(df, city_column, weight_column, maptype, title, color_series)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "date_column": "【日期字段名】",
        "open_column": "【开盘价字段名】",
        "high_column": "【最高价字段名】",
        "low_column": "【最低价字段名】",
        "close_column": "【收盘价字段名】",
        "volume_column": "【成交量字段名】",
    }
)
def zc_Kchart(
    data_frame: xlo.Array(),
    date_column: str,
    open_column: str,
    high_column: str,
    low_column: str,
    close_column: str,
    volume_column: str,
):
    """根据输入的表格数据生成K线图。
    示例
        =zc_Kchart(data_frame=data_frame, date_column="日期", open_column="开盘价", high_column="最高价", low_column="最低价", close_column="收盘价", volume_column="成交量")
    """
    from zhixinpy import func_kchart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    df[date_column] = df[date_column].apply(date2str)

    return func_kchart.draw_kchart(df, date_column, open_column, high_column, low_column, close_column, volume_column)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "src_column": "【出发字段名】",
        "dest_column": "【目的地字段名】",
        "weight_column": "【权重字段名】",
        "maptype": "【国内区域地图名，默认中国】可填 广东 上海 广州 等",
        "title": "【标题】",
    },
)
def zc_GeoLine(
    data_frame: xlo.Array(),
    src_column: str,
    dest_column: str,
    weight_column: str,
    maptype: str = "中国",
    title: str = "地图",
):
    """根据输入的表格数据生成地图数据。
    示例
        =zc_GeoLine(data_frame=data_frame, src_column="出发城市", dest_column="目的地城市", weight_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    if maptype in ["china", "china-cities"]:  # 标准化省级城市名称
        df[src_column] = df[src_column].apply(standardize_province_name)
        df[dest_column] = df[dest_column].apply(standardize_province_name)

    return func_chart.geoline(
        df, src_column, dest_column, weight_column, maptype, title
    )

@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "x": "【字段名】",
        "y": "【字段名】",
        "title": "【标题】",
    },
)
def zc_funnel(df: pd.DataFrame, x: str, y: str, title: str = "漏斗图"):
    """根据输入的表格数据生成漏斗图。
    示例
        =zc_funnel(data_frame=data_frame, x="步骤", y="数值")
    """
    from zhixinpy import func_chart

    return func_chart.funnel(df, x, y, title)

@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "city_column": "【城市字段名】",
        "weight_column": "【权重字段名】",
        "maptype": "【国内区域地图名，默认中国】可填 广东 上海 广州 等",
        "title": "【标题】",
    },
)
def zc_Map(
    data_frame: xlo.Array(),
    city_column: str,
    weight_column: str,
    maptype: str = "中国",
    title: str = "地图",
    color_series: str = '蓝色',
):
    """根据输入的表格数据生成地图数据。
    示例
        =zc_Map(data_frame=data_frame, city_column="城市", weight_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    if maptype in ["china", "china-cities"]:  # 标准化省级城市名称
        df[city_column] = df[city_column].apply(standardize_province_name)
    weight_column = date2str(weight_column)

    return func_chart.themap(df, city_column, weight_column, maptype, title, color_series)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "city_column": "【城市字段名】",
        "date_columns": "【日期字段名 序列】",
        "maptype": "【国内区域地图名，默认中国】可填 广东 上海 广州 等",
        "title": "【标题】",
    },
)
def zc_Map_ts(
    data_frame: xlo.Array(),
    city_column: str,
    date_columns: xlo.Array(),
    maptype: str = "中国",
    title: str = "地图",
):
    """根据输入的表格数据生成地图数据。
    示例
        =zc_Map(data_frame=data_frame, city_column="城市", weight_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    if maptype in ["china", "china-cities"]:  # 标准化省级城市名称
        df[city_column] = df[city_column].apply(standardize_province_name)
    date_columns = datelist2strlist(date_columns)

    return func_chart.map_ts(df, city_column, date_columns, maptype, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "x_column": "【x字段名】",
        "y_column": "【y字段名】",
        "z_column": "【z字段名】",
        "title": "【标题】",
    },
)
def zc_surface3d(
    data_frame: xlo.Array(),
    x_column: str,
    y_column: str,
    z_column: str = "",
    title: str = "",
):
    """根据输入的表格数据生成地图数据。
    示例
        =zc_surface3d(data_frame=data_frame, city_column="城市", weight_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")

    return func_chart.surface3d(df, x_column, y_column, z_column, title)


'''
def calendar_heatmap(df, date_column: str, value_column: str, orient: str="周", title: str = ""):
    from pyecharts.charts import Calendar
    from pyecharts.globals import ThemeType
    # 先准备数据，原本数据是df [[date_column], [value_column]] 要组织成
    # 如果orient=周 则是 组织为日历图中横轴是每年第几周，纵轴为周一到周日，值为value_column
    # 如果orient=月 则是 组织为日历图中横轴是每年第几月，纵轴为1到31，值为value_column

'''
@xlo.func(
    group="知心-图表",
    args={
        "df": "【带表头的表格，选择区域】待可视化的表格。",
        "date_column": "【日期字段名】",
        "value_column": "【数值字段名】",
        "orient": "【周/月】",
        "title": "【标题】",
    },
)
def zc_calendar_heatmap(df: xlo.Array(), date_column: str, value_column: str, orient: str="周", title: str = ""):
    # orient 周/月
    from zhixinpy import func_chart

    df = load_to_dataframe(df)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    # 把df[date_column] 转换为日期格式
    df[date_column] = df[date_column].apply(lambda x: xlo.from_excel_date(float(x)).strftime("%Y/%m/%d"))
    return func_chart.calendar_heatmap(df, date_column, value_column, orient, title)


@xlo.func
def zc_heart():

    from zhixinpy import func_chart

    # 参数范围
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    u, v = np.meshgrid(u, v)

    # 计算坐标
    x = 16 * np.sin(u) ** 3 * np.sin(v)
    y = (
        13 * np.cos(u) - 5 * np.cos(2 * u) - 2 * np.cos(3 * u) - np.cos(4 * u)
    ) * np.sin(v)
    z = 10 * np.cos(v)

    # 展平并组合为 [x, y, z] 格式
    points = np.column_stack((x.ravel(), y.ravel(), z.ravel()))
    point_list = points.tolist()  # 转为 Python list
    df = pd.DataFrame(point_list, columns=["x", "y", "z"])
    return func_chart.surface3d(df, x_column="x", y_column="y", z_column="z")


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "name_column": "【x字段名】",
        "value_column": "【y字段名】",
        "title": "【标题】",
    },
)
def zc_pie_bar(
    data_frame: xlo.Array(),
    name_column: str,
    value_column: str,
    title: str = "",
):
    """根据输入的表格数据生成饼图与柱状图。
    示例
        =zc_pie_bar(data_frame=data_frame, name_column="类型", value_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    value_column = date2str(value_column)

    return func_chart.pie_bar(df, name_column, value_column, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "name_column": "【x字段名】",
        "date_columns": "【日期字段名 list】",
        "title": "【标题】",
    },
)
def zc_pie_ts(
    data_frame: xlo.Array(),
    name_column: str,
    date_columns: xlo.Array(),
    title: str = "",
):
    """根据输入的表格数据生成饼图与柱状图。
    示例
        =zc_pie_ts(data_frame=data_frame, name_column="类型", date_columns="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    date_columns = datelist2strlist(date_columns)

    return func_chart.pie_ts(df, name_column, date_columns, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "city_column": "【城市字段名】",
        "value_column": "【数值字段名】",
        "maptype": "【国内区域地图名，默认中国】可填 广东 上海 广州 等",
        "title": "【标题】",
    },
)
def zc_map_bar(
    data_frame: xlo.Array(),
    city_column: str,
    value_column: str,
    maptype: str = "中国",
    title: str = "",
):
    """根据输入的表格数据生成饼图与柱状图。
    示例
        =zc_map_bar(data_frame=data_frame, city_column="类型", value_column="数值")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    if maptype in ["china", "china-cities"]:  # 标准化省级城市名称
        df[city_column] = df[city_column].apply(standardize_province_name)
    value_column = date2str(value_column)

    return func_chart.map_bar(df, city_column, value_column, maptype, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "title": "【标题】",
    },
)
def zc_bar_3d(
    data_frame: xlo.Array(),
    x_column: str,
    y_column: str,
    z_column: str,
    title: str = "",
):
    """根据输入的表格数据生成饼图与柱状图。
    示例
        =zc_bar_3d(data_frame=data_frame)
    """

    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")

    return func_chart.bar_3d(df, x_column, y_column, z_column, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "date_column": "【日期字段名】",
        "name_column": "【名称字段名】",
        "value_column": "【值字段名】",
        "limit": "【限制前N排名】",
        "title": "【标题】",
    },
)
def zc_rank(
    data_frame: xlo.Array(),
    date_column: str,
    name_column: str,
    value_column: str,
    limit: int = 10,
    title: str = "",
):
    """根据输入的表格数据生成排名图。
    示例
        =zc_rank(data_frame=data_frame, date_column='年份'，name_column="公司名", value_column="非货规模")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    value_column = date2str(value_column)

    return func_chart.rank(df, date_column, name_column, value_column, limit, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "date_columns": "【日期字段名，列表】可以选一个或多个日期字段",
        "name_column": "【名称字段名】",
        "limit": "【限制前N排名】",
        "title": "【标题】",
    },
)
def zc_rank_wind(
    data_frame: xlo.Array(),
    date_columns: xlo.Array(),
    name_column: str,
    limit: int = 10,
    title: str = "",
):
    """根据输入的表格数据生成排名图。Wind指标格式
    示例
        =zc_rank_wind(data_frame=data_frame, date_column='年份'，name_column="公司名")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")
    date_columns = datelist2strlist(date_columns)

    return func_chart.rank_wind(df, date_columns, name_column, limit, title)


@xlo.func(
    group="知心-图表",
    args={
        "data_frame": "【带表头的表格，选择区域】待可视化的表格。",
        "src_col": "【源字段名】",
        "dest_col": "【目标字段名】",
        "value_col": "【值字段名】",
        "category_col": "【分类字段名】",
    },
)
def zc_Network(
    data_frame: xlo.Array(),
    src_col: str,
    dest_col: str,
    value_col: str,
    category_col: str = None,
    src_size_col: str = None,
    dest_size_col: str = None,
):
    """根据输入的表格数据生成网络图。
    示例
        =zc_Network(data_frame=data_frame, src_col="城市", dest_col="城市", value_col="城市", category_col="城市")
    """
    from zhixinpy import func_chart

    df = load_to_dataframe(data_frame)
    if df.empty:
        raise ValueError("输入数据为空，请检查表格内容")

    return func_chart.draw_network(
        df, src_col, dest_col, value_col, category_col, src_size_col, dest_size_col
    )


############################### 资本市场行情 ##############################################
from zhixinpy.func_rtd import SinaQuote

_rtdServer = xlo.RtdServer()


class SinaQuoteRTD(xlo.RtdPublisher):
    _sinaQuote = SinaQuote()

    def __init__(self, symbol, field):
        super().__init__()  # You *must* call this explicitly or the python binding library will crash
        self.__symbol = symbol
        self.__field = field
        self._task = None

    def connect(self, num_subscribers):

        if self.done():

            async def run():
                await self._sinaQuote.subscribe(
                    self.__symbol, self.__field, self.__update
                )

            self._task = xlo.get_event_loop().create_task(run())

    def disconnect(self, num_subscribers):
        if num_subscribers == 0:

            async def run():
                await self._sinaQuote.unsubscribe(
                    self.__symbol, self.__field, self.__update
                )

            self._task = xlo.get_event_loop().create_task(run())
            self.stop()
            return True  # This publisher is no longer required: schedule it for destruction

    def stop(self):
        if self._task is not None:
            self._task.cancel()

    def done(self):
        return self._task is None or self._task.done()

    def topic(self):
        return f"{self.__symbol}-{self.__field}"

    async def __update(self, symbol, field, value, timestamp):
        await _rtdServer.publish(f"{self.__symbol}-{self.__field}", value)


@xlo.func(
    group="知心-行情",
    args={
        "symbol": "标的新浪代码，例如sh000001表示上证综指",
        "field": "[可选] 指标名，默认lastPrice最新价。 open-开盘价 preClose-昨收盘 high-最高价 low-最低价 volume-成交手数 turnOver-成交额 bidVolume1-买1量 bidPrice1-买1价 askVolume1-卖1量 askPrice1-卖1价",
    },
)
def zq_Realtime(symbol, field="lastPrice"):
    """返回实时行情，先调用zq_Realtime("sh000001")以订阅最新行情，才可以订阅其他字段
    示例
        =zq_Realtime("sh000001")
        =zq_Realtime("sh000001", "open")
    语法
        zq_Realtime(symbol, [field])
        data - 标的新浪代码。在这里查看支持的标的 https://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount
        field - [可选] - symbol-新浪代码 name-标的中文名 open-开盘价 preClose-昨收盘 lastPrice-最新价 high-最高价 low-最低价 volume-成交手数 turnOver-成交额 bidVolume1-买1量 bidPrice1-买1价 bidVolume2-买2量 bidPrice2-买2价 bidVolume3-买3量	bidPrice3-买3价	bidVolume4-买4量 bidPrice4-买4价 bidVolume5-买5量 bidPrice5-买5价 askVolume1-卖1量 askPrice1-买1价 askVolume2-卖2量 askPrice2-买2价	askVolume3-卖3量 askPrice3-买3价 askVolume4-卖4量 askPrice4-买4价 askVolume5-卖5量 askPrice5-买5价 date-成交日 time-成交时间
    """
    if symbol is None or len(str(symbol)) <= 0:
        return "错误：股票标的代码不能为空"
    if field == "lastPrice":  # 对于最新价字段而言
        if _rtdServer.peek(f"{symbol}-{field}") is None:  # 如果找不到，先要发布
            publisher = SinaQuoteRTD(symbol=symbol, field="lastPrice")
            _rtdServer.start(publisher)
        return _rtdServer.subscribe(f"{symbol}-{field}")  # 进行订阅
    else:  # 对于其他字段而言，先判断lastPrice有没有
        if _rtdServer.peek(f"{symbol}-{field}") is None:
            publisher = SinaQuoteRTD(symbol=symbol, field=field)
            _rtdServer.start(publisher)
        return _rtdServer.subscribe(f"{symbol}-{field}")


@xlo.func(
    group="知心-行情",
    args={
        "symbol": "新浪股票标的，如sh000001 全部列表在 https://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount",
        "mode": "[可选 - 默认值为 3] - 图片的调整大小模式。1：保持宽高比适合单元格。2：拉伸或压缩适合单元格。3：保持原始大小。4：自定义大小。",
        "height": "[可选] - 以像素为单位的图片高度。必须将模式的值设为 4，才能设置自定义高度。",
        "width": "[可选] - 以像素为单位的图片宽度。必须将模式的值设为 4，才能设置自定义宽度。",
    },
)
def zq_DailyK(symbol, mode=3, height=None, width=None):
    """插入日K图，数据来源：新浪财经
    示例
        =zq_DailyK("sh000001")
    """
    if symbol is None or len(str(symbol)) <= 0:
        return "错误：股票标的代码不能为空"
    if mode not in (1, 2, 3, 4):
        return "错误：mode只能在1 2 3 4之中选取"
    from zhixinpy import func_tools

    if mode == 4:
        if height <= 0:
            return "错误：height必须是正整数"
        if width <= 0:
            return "错误：width必须是正整数"
    image = func_tools.azImage(
        url=f"http://image.sinajs.cn/newchart/daily/n/{symbol}.gif"
    )
    _set_image_size(image, mode, height, width)
    return ""


@xlo.func(
    group="知心-行情",
    args={
        "symbol": "新浪股票标的，如sh000001 全部列表在 https://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount",
        "mode": "[可选 - 默认值为 3] - 图片的调整大小模式。1：保持宽高比适合单元格。2：拉伸或压缩适合单元格。3：保持原始大小。4：自定义大小。",
        "height": "[可选] - 以像素为单位的图片高度。必须将模式的值设为 4，才能设置自定义高度。",
        "width": "[可选] - 以像素为单位的图片宽度。必须将模式的值设为 4，才能设置自定义宽度。",
    },
)
def zq_WeeklyK(symbol, mode=3, height=None, width=None):
    """插入周K图，数据来源：新浪财经
    示例
        =zq_WeeklyK("sh000001")
    """
    if symbol is None or len(str(symbol)) <= 0:
        return "错误：股票标的代码不能为空"
    if mode not in (1, 2, 3, 4):
        return "错误：mode只能在1 2 3 4之中选取"
    from zhixinpy import func_tools

    if mode == 4:
        if height <= 0:
            return "错误：height必须是正整数"
        if width <= 0:
            return "错误：width必须是正整数"
    image = func_tools.azImage(
        url=f"http://image.sinajs.cn/newchart/weekly/n/{symbol}.gif"
    )
    _set_image_size(image, mode, height, width)
    return ""


@xlo.func(
    group="知心-行情",
    args={
        "symbol": "新浪股票标的，如sh000001 全部列表在 https://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount",
        "mode": "[可选 - 默认值为 3] - 图片的调整大小模式。1：保持宽高比适合单元格。2：拉伸或压缩适合单元格。3：保持原始大小。4：自定义大小。",
        "height": "[可选] - 以像素为单位的图片高度。必须将模式的值设为 4，才能设置自定义高度。",
        "width": "[可选] - 以像素为单位的图片宽度。必须将模式的值设为 4，才能设置自定义宽度。",
    },
)
def zq_MonthlyK(symbol, mode=3, height=None, width=None):
    """插入月K图，数据来源：新浪财经
    示例
        =zq_MonthlyK("sh000001")
    """
    if symbol is None or len(str(symbol)) <= 0:
        return "错误：股票标的代码不能为空"
    if mode not in (1, 2, 3, 4):
        return "错误：mode只能在1 2 3 4之中选取"
    from zhixinpy import func_tools

    if mode == 4:
        if height <= 0:
            return "错误：height必须是正整数"
        if width <= 0:
            return "错误：width必须是正整数"
    image = func_tools.azImage(
        url=f"http://image.sinajs.cn/newchart/monthly/n/{symbol}.gif"
    )
    _set_image_size(image, mode, height, width)
    return ""


@xlo.func(
    group="知心-行情",
    args={
        "symbol": "新浪股票标的，如sh000001 全部列表在 https://vip.stock.finance.sina.com.cn/mkt/#stock_hs_amount",
        "mode": "[可选 - 默认值为 3] - 图片的调整大小模式。1：保持宽高比适合单元格。2：拉伸或压缩适合单元格。3：保持原始大小。4：自定义大小。",
        "height": "[可选] - 以像素为单位的图片高度。必须将模式的值设为 4，才能设置自定义高度。",
        "width": "[可选] - 以像素为单位的图片宽度。必须将模式的值设为 4，才能设置自定义宽度。",
    },
)
def zq_MinuteK(symbol, mode=3, height=None, width=None):
    """插入日内分时图，数据来源：新浪财经
    示例
        =zq_MinuteK("sh000001")
    """
    if symbol is None or len(str(symbol)) <= 0:
        return "错误：股票标的代码不能为空"
    if mode not in (1, 2, 3, 4):
        return "错误：mode只能在1 2 3 4之中选取"
    from zhixinpy import func_tools

    if mode == 4:
        if height <= 0:
            return "错误：height必须是正整数"
        if width <= 0:
            return "错误：width必须是正整数"
    image = func_tools.azImage(
        url=f"http://image.sinajs.cn/newchart/min/n/{symbol}.gif"
    )
    _set_image_size(image, mode, height, width)
    return ""


############################### FUNCTION  END ##############################################
