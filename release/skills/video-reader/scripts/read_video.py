"""
Video Reader — Extract frames + OCR từ video
Hỗ trợ: mp4, avi, mov, webm, mkv
"""
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent

def check_opencv():
    try:
        import cv2
        return True
    except ImportError:
        return False

def install_opencv():
    print("[*] Installing opencv-python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "-q"])
    print("[+] Done!")

def get_video_info(video_path):
    """Lấy thông tin video: duration, fps, resolution"""
    import cv2
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    
    cap.release()
    return {
        "fps": round(fps, 2),
        "frames": frame_count,
        "width": width,
        "height": height,
        "duration_sec": round(duration, 1),
        "duration_str": f"{int(duration//60)}:{int(duration%60):02d}"
    }

def extract_frames(video_path, output_dir, interval=2, max_frames=20):
    """Extract frames từ video mỗi interval giây"""
    import cv2
    
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frames_saved = []
    frame_interval = int(fps * interval)  # mỗi interval giây
    
    for i, target_frame in enumerate(range(0, total_frames, frame_interval)):
        if i >= max_frames:
            break
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = cap.read()
        if not ret:
            break
        
        timestamp_sec = target_frame / fps
        filename = f"frame_{timestamp_sec:.1f}s.png"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, frame)
        
        frames_saved.append({
            "timestamp_sec": round(timestamp_sec, 1),
            "timestamp_str": f"{int(timestamp_sec//60)}:{int(timestamp_sec%60):02d}",
            "file": filename,
            "path": filepath
        })
        print(f"  [frame {i+1}] {timestamp_sec:.1f}s → {filename}")
    
    cap.release()
    return frames_saved

def ocr_frames(frames, output_dir):
    """OCR từng frame bằng EasyOCR"""
    try:
        import easyocr
    except ImportError:
        print("[*] Installing easyocr...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "easyocr", "-q"])
        import easyocr
    
    print("[*] Loading EasyOCR (first run may download model)...")
    reader = easyocr.Reader(['en'], gpu=False)
    
    all_text = []
    
    for i, frame in enumerate(frames):
        print(f"  [OCR {i+1}/{len(frames)}] {frame['timestamp_str']} ...", end=" ")
        try:
            results = reader.readtext(frame['path'], detail=0)
            text = " ".join(results).strip()
            frame['ocr_text'] = text
            all_text.append(f"[{frame['timestamp_str']}] {text}")
            print(f"→ {len(text)} chars")
        except Exception as e:
            frame['ocr_text'] = ""
            print(f"→ error: {e}")
    
    # Lưu text
    text_file = os.path.join(output_dir, "ocr_text.txt")
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(all_text))
    
    return all_text, text_file

def main():
    parser = argparse.ArgumentParser(description="Read video content via OCR")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--interval", type=float, default=2, help="Seconds between frames (default: 2)")
    parser.add_argument("--max-frames", type=int, default=20, help="Max frames to extract (default: 20)")
    parser.add_argument("--output", default=None, help="Output directory")
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR, only extract frames")
    args = parser.parse_args()
    
    video_path = args.video
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        sys.exit(1)
    
    # Output dir
    video_name = Path(video_path).stem
    output_dir = args.output or os.path.join(os.path.dirname(video_path), f"{video_name}_analysis")
    frames_dir = os.path.join(output_dir, "frames")
    
    # Check opencv
    if not check_opencv():
        print("[!] opencv-python not installed.")
        install_opencv()
    
    import cv2
    
    print(f"🎬 Video: {video_path}")
    
    # Info
    info = get_video_info(video_path)
    if not info:
        print("❌ Cannot open video!")
        sys.exit(1)
    
    print(f"   📏 {info['width']}x{info['height']} | {info['fps']}fps")
    print(f"   ⏱  {info['duration_str']} ({info['frames']} frames)")
    print()
    
    # Extract frames
    print(f"[1] Extracting frames (every {args.interval}s, max {args.max_frames})...")
    frames = extract_frames(video_path, frames_dir, args.interval, args.max_frames)
    print(f"   ✅ {len(frames)} frames saved to {frames_dir}")
    print()
    
    if args.no_ocr:
        # Lưu summary
        summary = {
            "video": video_path,
            "info": info,
            "frames": [{"timestamp_str": f['timestamp_str'], "file": f['file']} for f in frames]
        }
        summary_file = os.path.join(output_dir, "summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"✅ Summary saved to {summary_file}")
        return
    
    # OCR
    print(f"[2] OCR {len(frames)} frames...")
    all_text, text_file = ocr_frames(frames, output_dir)
    print()
    
    # Summary
    summary = {
        "video": video_path,
        "info": info,
        "frames": [{
            "timestamp_str": f['timestamp_str'],
            "file": f['file'],
            "text": f.get('ocr_text', '')
        } for f in frames],
        "full_text": "\n\n".join(all_text)
    }
    summary_file = os.path.join(output_dir, "summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print(f"✅ DONE! Output: {output_dir}")
    print(f"   📄 OCR text: {text_file}")
    print(f"   📋 Summary:  {summary_file}")
    print(f"   🖼  Frames:   {frames_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
