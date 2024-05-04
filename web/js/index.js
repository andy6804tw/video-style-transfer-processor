document.getElementById("imgDemo").src = `./image/demo${
  Math.floor(Math.random() * 4) + 1
}.gif`;

/** Post File */
const addFile = () => {
  // File
  const formData = new FormData();
  const vildeoFile = document.getElementById("videoFile").files;
  const imageFile = document.getElementById("imageFile").files;
  if (vildeoFile.length) {
    // Get video file
    formData.append("file", vildeoFile[0]);
    formData.append("styleImage", imageFile[0]);
    console.log("innn");
    // 上傳 Image 檔案
    axios
      .post(`https://video-style-transfer-processor.onrender.com/style`, formData, {
        headers: {
          "content-type": "mutipart/form-data",
        },
      })
      .then(function (response) {
        var dataObject = response.data;
        console.log("done");
        // Render result video
        const videoPlayerRes = document.getElementById("videoPlayer-res");
        videoPlayerRes.innerHTML = "";
        videoPlayerRes.classList.remove("d-none");
        const playerRes = videojs("videoPlayer-res", {
          sources: [{ src: `https://video-style-transfer-processor.onrender.com/static/output.mp4` }],
          loop: false,
          autoplay: "muted",
          controls: true,
        });
      });
  }
};
