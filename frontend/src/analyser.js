// ===== OpenCV.js Image Analysis =====
// This script handles client-side image quality analysis using OpenCV.js
// It runs before sending images to the server to improve quality and reduce costs

let cvReady = false;
let opencvLoaded = false;

// Initialize OpenCV.js
function initOpenCV() {
    if (typeof cv !== 'undefined' && !opencvLoaded) {
        cvReady = true;
        opencvLoaded = true;
        console.log('OpenCV.js loaded and ready');
    }
}

// Check if OpenCV is ready
function isOpenCVReady() {
    return cvReady && typeof cv !== 'undefined';
}

// Wait for OpenCV to be loaded
function waitForOpenCV(callback, maxAttempts = 50, delay = 100) {
    let attempts = 0;
    
    function check() {
        if (isOpenCVReady()) {
            callback();
        } else if (attempts < maxAttempts) {
            attempts++;
            setTimeout(check, delay);
        } else {
            console.warn('OpenCV.js not loaded after maximum attempts');
            // Still try to proceed with basic checks
            callback();
        }
    }
    
    check();
}

// Main image analysis function
function analyzeImageQuality(file, callback) {
    if (!file || !file.type.startsWith('image/')) {
        callback({ isGood: true, reason: '' });
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            performImageAnalysis(img, callback);
        };
        img.onerror = function() {
            callback({ isGood: false, reason: 'Erreur de chargement' });
        };
        img.src = e.target.result;
    };
    reader.onerror = function() {
        callback({ isGood: false, reason: 'Erreur de lecture' });
    };
    reader.readAsDataURL(file);
}

// Perform comprehensive image analysis
function performImageAnalysis(img, callback) {
    // Basic checks without OpenCV
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    
    // Check resolution
    const minResolution = 300;
    const hasGoodResolution = img.width >= minResolution && img.height >= minResolution;
    
    if (!hasGoodResolution) {
        callback({
            isGood: false,
            reason: `Résolution trop faible (${img.width}x${img.height}), minimum ${minResolution}x${minResolution}`,
            width: img.width,
            height: img.height
        });
        return;
    }
    
    // Check aspect ratio (too wide or too tall)
    const aspectRatio = img.width / img.height;
    const maxAspectRatio = 3;
    const minAspectRatio = 1 / maxAspectRatio;
    
    if (aspectRatio > maxAspectRatio || aspectRatio < minAspectRatio) {
        callback({
            isGood: false,
            reason: `Ratio d'aspect extrême (${aspectRatio.toFixed(2)})`,
            width: img.width,
            height: img.height
        });
        return;
    }
    
    // Check file size
    const maxFileSize = 10 * 1024 * 1024; // 10MB
    if (file && file.size > maxFileSize) {
        callback({
            isGood: false,
            reason: `Fichier trop volumineux (${(file.size / 1024 / 1024).toFixed(1)}MB)`,
            width: img.width,
            height: img.height
        });
        return;
    }
    
    // Try OpenCV analysis if available
    if (isOpenCVReady()) {
        try {
            performOpenCVAnalysis(canvas, imageData, callback);
        } catch (e) {
            console.warn('OpenCV analysis failed:', e);
            // Fallback to basic checks
            callback({
                isGood: true,
                reason: '',
                width: img.width,
                height: img.height
            });
        }
    } else {
        // Basic checks passed
        callback({
            isGood: true,
            reason: '',
            width: img.width,
            height: img.height
        });
    }
}

// Advanced analysis using OpenCV.js
function performOpenCVAnalysis(canvas, imageData, callback) {
    try {
        // Convert ImageData to cv.Mat
        const src = cv.matFromImageData(imageData);
        const dst = new cv.Mat();
        
        // Convert to grayscale
        cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
        
        // Check brightness
        const mean = cv.mean(dst);
        const brightness = mean[0];
        
        // Check contrast using standard deviation
        const meanMat = new cv.Mat();
        const stdDevMat = new cv.Mat();
        cv.meanStdDev(dst, meanMat, stdDevMat);
        const stdDev = stdDevMat.doubleAt(0);
        
        // Check sharpness using Laplacian
        const laplacian = new cv.Mat();
        cv.Laplacian(dst, laplacian, cv.CV_64F);
        const variance = cv.mean(laplacian)[0];
        
        // Clean up
        src.delete();
        dst.delete();
        meanMat.delete();
        stdDevMat.delete();
        laplacian.delete();
        
        // Evaluate quality
        const results = {
            brightness: brightness,
            contrast: stdDev,
            sharpness: variance,
            isGood: true,
            reason: '',
            width: canvas.width,
            height: canvas.height
        };
        
        // Brightness check (0-255 scale)
        const minBrightness = 30;
        const maxBrightness = 220;
        if (brightness < minBrightness || brightness > maxBrightness) {
            results.isGood = false;
            results.reason = brightness < minBrightness ? 'Image trop sombre' : 'Image trop claire';
        }
        
        // Contrast check
        const minContrast = 15;
        if (stdDev < minContrast) {
            results.isGood = false;
            results.reason = 'Contraste faible';
        }
        
        // Sharpness check
        const minSharpness = 30;
        if (variance < minSharpness) {
            results.isGood = false;
            results.reason = 'Image floue';
        }
        
        callback(results);
        
    } catch (error) {
        console.warn('OpenCV analysis error:', error);
        callback({
            isGood: true,
            reason: '',
            width: canvas.width,
            height: canvas.height
        });
    }
}

// Enhance image quality using OpenCV.js
function enhanceImageClientSide(file, callback) {
    if (!isOpenCVReady()) {
        callback(file);
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            try {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                
                const src = cv.matFromImageData(ctx.getImageData(0, 0, canvas.width, canvas.height));
                const dst = new cv.Mat();
                
                // Convert to grayscale
                cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
                
                // Apply adaptive thresholding
                cv.adaptiveThreshold(dst, dst, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2);
                
                // Convert back to RGBA
                cv.cvtColor(dst, src, cv.COLOR_GRAY2RGBA);
                
                // Update canvas
                cv.imshow(canvas, src);
                
                // Convert to blob
                canvas.toBlob(function(blob) {
                    const enhancedFile = new File([blob], 'enhanced_' + file.name, { type: 'image/jpeg' });
                    callback(enhancedFile);
                }, 'image/jpeg', 0.9);
                
                // Clean up
                src.delete();
                dst.delete();
                
            } catch (error) {
                console.warn('Image enhancement failed:', error);
                callback(file);
            }
        };
        img.onerror = function() {
            callback(file);
        };
        img.src = e.target.result;
    };
    reader.onerror = function() {
        callback(file);
    };
    reader.readAsDataURL(file);
}

// Crop image to remove empty borders
function cropImageToContent(file, callback) {
    if (!isOpenCVReady()) {
        callback(file);
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            try {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                
                const src = cv.matFromImageData(ctx.getImageData(0, 0, canvas.width, canvas.height));
                const gray = new cv.Mat();
                const binary = new cv.Mat();
                
                // Convert to grayscale
                cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);
                
                // Threshold to find content
                cv.threshold(gray, binary, 240, 255, cv.THRESH_BINARY_INV);
                
                // Find contours
                const contours = new cv.MatVector();
                const hierarchy = new cv.Mat();
                cv.findContours(binary, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
                
                if (contours.size() > 0) {
                    // Find bounding box of all contours
                    let minX = canvas.width, minY = canvas.height;
                    let maxX = 0, maxY = 0;
                    
                    for (let i = 0; i < contours.size(); i++) {
                        const contour = contours.get(i);
                        const rect = cv.boundingRect(contour);
                        
                        minX = Math.min(minX, rect.x);
                        minY = Math.min(minY, rect.y);
                        maxX = Math.max(maxX, rect.x + rect.width);
                        maxY = Math.max(maxY, rect.y + rect.height);
                    }
                    
                    // Add some padding
                    const padding = 20;
                    minX = Math.max(0, minX - padding);
                    minY = Math.max(0, minY - padding);
                    maxX = Math.min(canvas.width, maxX + padding);
                    maxY = Math.min(canvas.height, maxY + padding);
                    
                    const width = maxX - minX;
                    const height = maxY - minY;
                    
                    // Only crop if it removes significant empty space
                    if (width < canvas.width * 0.9 || height < canvas.height * 0.9) {
                        const croppedCanvas = document.createElement('canvas');
                        croppedCanvas.width = width;
                        croppedCanvas.height = height;
                        const croppedCtx = croppedCanvas.getContext('2d');
                        croppedCtx.drawImage(canvas, minX, minY, width, height, 0, 0, width, height);
                        
                        croppedCanvas.toBlob(function(blob) {
                            const croppedFile = new File([blob], 'cropped_' + file.name, { type: 'image/jpeg' });
                            callback(croppedFile);
                        }, 'image/jpeg', 0.9);
                        
                        // Clean up
                        src.delete();
                        gray.delete();
                        binary.delete();
                        contours.delete();
                        hierarchy.delete();
                        return;
                    }
                }
                
                // If no cropping needed, return original
                callback(file);
                
                // Clean up
                src.delete();
                gray.delete();
                binary.delete();
                contours.delete();
                hierarchy.delete();
                
            } catch (error) {
                console.warn('Image cropping failed:', error);
                callback(file);
            }
        };
        img.onerror = function() {
            callback(file);
        };
        img.src = e.target.result;
    };
    reader.onerror = function() {
        callback(file);
    };
    reader.readAsDataURL(file);
}

// Check if image is rotated (EXIF orientation)
function checkImageOrientation(file, callback) {
    // Note: EXIF reading requires additional libraries
    // For now, we'll assume the image is correctly oriented
    callback({ isRotated: false, orientation: 1 });
}

// Rotate image if needed
function rotateImage(file, degrees, callback) {
    if (degrees === 0) {
        callback(file);
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas dimensions based on rotation
            if (degrees === 90 || degrees === 270) {
                canvas.width = img.height;
                canvas.height = img.width;
            } else {
                canvas.width = img.width;
                canvas.height = img.height;
            }
            
            // Rotate and draw
            ctx.save();
            if (degrees === 90) {
                ctx.translate(canvas.width, 0);
                ctx.rotate(Math.PI / 2);
            } else if (degrees === 180) {
                ctx.translate(canvas.width, canvas.height);
                ctx.rotate(Math.PI);
            } else if (degrees === 270) {
                ctx.translate(0, canvas.height);
                ctx.rotate(-Math.PI / 2);
            }
            ctx.drawImage(img, 0, 0, img.width, img.height);
            ctx.restore();
            
            canvas.toBlob(function(blob) {
                const rotatedFile = new File([blob], 'rotated_' + file.name, { type: 'image/jpeg' });
                callback(rotatedFile);
            }, 'image/jpeg', 0.9);
        };
        img.onerror = function() {
            callback(file);
        };
        img.src = e.target.result;
    };
    reader.onerror = function() {
        callback(file);
    };
    reader.readAsDataURL(file);
}

// Public API
window.analyzeImageQuality = analyzeImageQuality;
window.enhanceImageClientSide = enhanceImageClientSide;
window.cropImageToContent = cropImageToContent;
window.checkImageOrientation = checkImageOrientation;
window.rotateImage = rotateImage;

// Initialize when OpenCV is loaded
if (typeof cv !== 'undefined') {
    initOpenCV();
} else {
    // Wait for OpenCV to load
    document.addEventListener('DOMContentLoaded', () => {
        // Check periodically
        const checkOpenCV = setInterval(() => {
            if (typeof cv !== 'undefined') {
                initOpenCV();
                clearInterval(checkOpenCV);
            }
        }, 100);
    });
}
