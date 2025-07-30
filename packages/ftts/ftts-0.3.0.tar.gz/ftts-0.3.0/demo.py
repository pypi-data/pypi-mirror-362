import requests
from pathlib import Path

import gradio as gr
import numpy as np
from wuba_wos import WOS
import time


MODEL = None
base_url = "http://ol-lbg-huangye.wpai.58dns.org:8867"
task_id = "21058"
tts_first_response_time = None
wos = WOS(
    bucket="voiceclone",
    app_id="lMpIhGfEdlnO",
    secret_id="41D9SCQPZErtk8xKsRgfC6hAnNBuSkz6",
)


def list_voice() -> list[str]:
    url = base_url + "/audio_roles"
    res = requests.get(url=url, headers={"taskid": task_id})
    voices = list(res.json()["roles"])
    if "后羿" in voices:
        voices.remove("后羿")
    if "殷夫人" in voices:
        voices.remove("殷夫人")
    if "赞助商" in voices:
        voices.remove("赞助商")
    return voices


def upload_voice(audio, name):
    voices = list_voice()
    if name in voices:
        return "音色已存在,请更改名称。"
    url = base_url + "/add_speaker"
    files = {"audio_file": (audio, open(audio, "rb"), "audio/wav")}
    data = {"name": name, "audio_file": audio}
    res = requests.post(url=url, headers={"taskid": task_id}, data=data, files=files)
    success = res.json()["success"]
    if success:
        msg = f"✅ 已成功上传音色 **{name}**"
        audio_type = Path(audio).suffix
        audio_name = name + audio_type
        try:
            res = wos.upload(audio_name, audio)
        except:
            return "上传到wos失败"
        return msg
    else:
        msg = "上传音频失败"
        return msg


def generate_voice(text: str, voice: str, pitch: float, speed: float):
    if isinstance(voice, list):
        voice = voice[0]
    url = base_url + "/speak"
    data = {
        "text": text,
        "name": voice,
        "pitch": pitch,
        "speed": speed,
        "stream": True,
        "response_format": "pcm",
        "sample_rate": 16000,
    }
    global tts_first_response_time
    tts_first_response_time = None
    start_time = time.time()
    res = requests.post(url=url, headers={"taskid": task_id}, json=data, stream=True)
    buffer = b""
    for chunk in res.iter_content(chunk_size=1024):
        if tts_first_response_time is None:
            tts_first_response_time = time.time() - start_time
        buffer += chunk
    if res.status_code != 200:
        return f"synthesize failed with status code {res.status_code}"
    audio = np.frombuffer(buffer, dtype=np.int16)
    return (16000, audio), f"首帧延迟: {round(tts_first_response_time, 4)}s"


def build_ui():
    with gr.Blocks() as demo:
        # Use HTML for centered title
        gr.HTML('<h1 style="text-align: center;">语音合成体验Demo</h1>')
        with gr.Tabs():
            # Voice Clone Tab
            with gr.TabItem("录制音色"):
                gr.Markdown(
                    "### 请在安静的环境，录制一段10s-20s左右的音频，可以参考阅读下面的内容。"
                )

                gr.Textbox(
                    "喂，你好，保洁公司。\n喂，你好，没听清你说的什么。\n好的，您是要窗帘清洗服务吗？\n那咱窗帘是什么材质的呀？\n好嘞，您家在哪个区呢？\n好的，窗帘有顽固污渍要清洗吗？"
                )

                with gr.Row():
                    prompt_wav_record = gr.Audio(
                        sources="microphone",
                        type="filepath",
                        label="录制音频.",
                        waveform_options=gr.WaveformOptions(sample_rate=16000),
                    )

                with gr.Row():
                    voice_name = gr.Textbox(
                        label="音色名称", lines=3, placeholder="输入音色名称"
                    )

                generate_buttom_clone = gr.Button("点击上传")
                result = gr.Markdown()
                generate_buttom_clone.click(
                    upload_voice, inputs=[prompt_wav_record, voice_name], outputs=result
                )

            with gr.TabItem("上传音色"):
                gr.Markdown("### 上传已录制的音色")

                with gr.Row():
                    prompt_wav_record = gr.Audio(
                        sources="upload",
                        type="filepath",
                        label="上传音频,格式为wav或者mp3",
                        waveform_options=gr.WaveformOptions(sample_rate=16000),
                    )

                with gr.Row():
                    voice_name = gr.Textbox(
                        label="音色名称", lines=3, placeholder="输入音色名称"
                    )

                generate_buttom_clone = gr.Button("点击上传")
                result = gr.Markdown()
                generate_buttom_clone.click(
                    upload_voice, inputs=[prompt_wav_record, voice_name], outputs=result
                )

            # Voice Creation Tab
            with gr.TabItem("语音合成"):
                gr.Markdown("### 选择音色并合成语音")
                voice = gr.Radio(choices=[])
                get_voices_button = gr.Button("刷新音色列表")

                @get_voices_button.click(outputs=voice)
                def show_dropdown(voice: gr.State):
                    voices = list_voice()
                    return gr.Radio(choices=voices)

                with gr.Row():
                    with gr.Column():
                        pitch = gr.Radio(
                            ["very_low", "low", "moderate", "high", "very_high"],
                            label="音高",
                            value="moderate",
                        )
                        speed = gr.Radio(
                            ["very_low", "low", "moderate", "high", "very_high"],
                            label="语速",
                            value="moderate",
                        )
                    with gr.Column():
                        text_input_creation = gr.Textbox(
                            value="你好，我是五八同城智能语音助手。",
                            label="待合成文本",
                            lines=3,
                            placeholder="请输入文本",
                        )
                        create_button = gr.Button("开始合成")

                audio_output = gr.Audio(
                    label="Generated Audio",
                    autoplay=False,
                    streaming=True,
                    type="numpy",
                    waveform_options=gr.WaveformOptions(sample_rate=16000),
                )
                show_ttfd = gr.Markdown(label="TTFD")
                create_button.click(
                    generate_voice,
                    inputs=[text_input_creation, voice, pitch, speed],
                    outputs=[audio_output, show_ttfd],
                )

    return demo


if __name__ == "__main__":
    # Build the Gradio demo by specifying the model directory and GPU device
    demo = build_ui()

    # Launch Gradio with the specified server name and port
    demo.launch(server_name="0.0.0.0", server_port=8081)
