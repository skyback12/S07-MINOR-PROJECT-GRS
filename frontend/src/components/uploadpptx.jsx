import React, { useState } from 'react';
import axios from 'axios';

function PptxUploader({ setIsUploading }) {
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && selectedFile.name.endsWith(".pptx")) {
            setFile(selectedFile);
            setUploadStatus("");
        } else {
            setUploadStatus("Please upload a valid .pptx file.");
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setUploadStatus("No file selected.");
            return;
        }

        setIsLoading(true);
        const formData = new FormData();
        formData.append("pptxFile", file);

        try {
            const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            if (response.status === 200) {
                setUploadStatus("File uploaded successfully!");
                setTimeout(() => setIsUploading(false), 3000);  // Close uploader after delay
            } else {
                setUploadStatus("File upload failed. Please try again.");
            }
        } catch (error) {
            setUploadStatus("File upload failed.");
            console.error("Error uploading file:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h2>Upload a .pptx file</h2>
            <input type="file" accept=".pptx" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={isLoading || !file}>
                {isLoading ? "Uploading..." : "Upload"}
            </button>
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
}

export default PptxUploader;
