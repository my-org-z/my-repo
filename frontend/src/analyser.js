// OpenCV.js Initialization
let cvReady = false;
let cv = null;

// Wait for OpenCV.js to load
function onOpenCVReady() {
    cv = window.cv;
    cv['onRuntimeInitialized'] = () => {
        cvReady = true;
        console.log('OpenCV.js is ready');
    };
}

// Check if OpenCV is loaded
function waitForOpenCV(callback) {
    if (cvReady) {
        callback();
    } else {
        // Check every 100ms
        const interval = setInterval(() => {
            if (cvReady) {
                clearInterval(interval);
                callback();
            }
        }, 100);
    }
}

// Analyze image quality using OpenCV.js
function analyzeImageQuality(imageFile, callback) {
    waitForOpenCV(() => {
        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);

            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const src = cv.matFromImageData(imageData);

            // Convert to grayscale
            const gray = new cv.Mat();
            cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);

            // Calculate sharpness (Laplacian Variance)
            const laplacian = new cv.Mat();
            cv.Laplacian(gray, laplacian, cv.CV_64F);
            const mean = new cv.Mat();
            const stddev = new cv.Mat();
            cv.meanStdDev(laplacian, mean, stddev);
            const variance = stddev.doubleAt(0) ** 2;

            // Calculate brightness
            const meanGray = new cv.Mat();
            cv.mean(gray, meanGray);
            const brightness = meanGray.doubleAt(0);

            // Calculate contrast
            const stddevGray = new cv.Mat();
            cv.meanStdDev(gray, new cv.Mat(), stddevGray);
            const contrast = stddevGray.doubleAt(0);

            // Clean up
            src.delete();
            gray.delete();
            laplacian.delete();
            mean.delete();
            stddev.delete();
            meanGray.delete();
            stddevGray.delete();

            // Quality thresholds
            const isSharp = variance > 50;
            const isBrightEnough = brightness > 50 && brightness < 200;
            const isGoodContrast = contrast > 20;
            const isHighRes = img.width >= 300 && img.height >= 300;

            let reason = '';
            if (!isSharp) reason = 'Image floue';
            else if (!isBrightEnough) reason = 'Luminosité incorrecte';
            else if (!isGoodContrast) reason = 'Contraste faible';
            else if (!isHighRes) reason = `Résolution trop faible (${img.width}x${img.height})`;

            callback({
                isGood: isSharp && isBrightEnough && isGoodContrast && isHighRes,
                variance,
                brightness,
                contrast,
                resolution: { width: img.width, height: img.height },
                reason
            });
        };
        img.src = URL.createObjectURL(imageFile);
    });
}

// Enhance image using OpenCV.js
function enhanceImageWithOpenCV(imageFile, callback) {
    waitForOpenCV(() => {
        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);

            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const src = cv.matFromImageData(imageData);

            // Convert to grayscale
            const gray = new cv.Mat();
            cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);

            // Adaptive thresholding
            const thresh = new cv.Mat();
            cv.adaptiveThreshold(gray, thresh, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2);

            // Find contours
            const contours = new cv.MatVector();
            const hierarchy = new cv.Mat();
            cv.findContours(thresh, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);

            let processedImg = src.clone();

            if (contours.size() > 0) {
                // Find largest contour
                let largestContour = null;
                let maxArea = 0;
                for (let i = 0; i < contours.size(); i++) {
                    const contour = contours.get(i);
                    const area = cv.contourArea(contour);
                    if (area > maxArea) {
                        maxArea = area;
                        largestContour = contour;
                    }
                }

                if (largestContour) {
                    const rect = cv.boundingRect(largestContour);
                    const cropped = src.roi(rect);

                    // Resize if too small
                    if (rect.width < 300 || rect.height < 300) {
                        const dsize = new cv.Size(0, 0);
                        dsize.width = rect.width * 2;
                        dsize.height = rect.height * 2;
                        cv.resize(cropped, processedImg, dsize, 0, 0, cv.INTER_LINEAR);
                    } else {
                        processedImg = cropped;
                    }

                    largestContour.delete();
                }
            }

            // Clean up
            src.delete();
            gray.delete();
            thresh.delete();
            contours.delete();
            hierarchy.delete();

            // Convert back to image
            const resultCanvas = document.createElement('canvas');
            resultCanvas.width = processedImg.cols;
            resultCanvas.height = processedImg.rows;
            const resultCtx = resultCanvas.getContext('2d');
            const resultImageData = new ImageData(
                new Uint8ClampedArray(processedImg.data),
                processedImg.cols,
                processedImg.rows
            );
            resultCtx.putImageData(resultImageData, 0, 0);

            processedImg.delete();

            callback(resultCanvas.toDataURL('image/jpeg', 0.9));
        };
        img.src = URL.createObjectURL(imageFile);
    });
}

// Initialize OpenCV when script loads
if (window.cv) {
    onOpenCVReady();
} else {
    // Load OpenCV.js if not already loaded
    const script = document.createElement('script');
    script.src = 'https://docs.opencv.org/4.7.0/opencv.js';
    script.async = true;
    script.onload = onOpenCVReady;
    document.body.appendChild(script);
}
