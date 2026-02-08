# 🎨 Bauhaus Image Rotation System - ACTIVE

## ✅ System Status: RUNNING

Your images are now in the **assets/** folder and will automatically rotate every **2 days**.

## 📸 Current Images

Run this to check current images:

```bash
python -c "from image_tracker import get_current_images, get_time_remaining; print('Current:', get_current_images()); print('Next rotation:', get_time_remaining())"
```

Current files in assets:

- `balloon_20260208_231744_1.png` (rectangle-based balloon)
- `balloon_20260208_231744_2.png` (rectangle-based balloon)

## 🔄 How Rotation Works

### Automatic (Every 2 Days):

```bash
python update_readme.py
```

**What happens:**

1. ✅ Checks if 2 days have passed
2. ✅ If yes: **Deletes old images**
3. ✅ **Generates 2 NEW images** with:
   - Random theme selection (balloon or mn+)
   - Random style variation per theme
   - Different seed = **unique placement & arrangement**
   - All made from **rectangles only**
   - **Bauhaus colors & symmetry**
4. ✅ Updates tracker with new 2-day timer
5. ✅ Updates README with stats and random image

### Manual (For Testing):

```bash
python force_regenerate.py
```

Forces immediate regeneration (bypasses 2-day wait)

## 🎯 Design Variations

### Balloon Theme (3 Random Styles):

1. **Composed**: Symmetric rectangles forming oval
2. **Stacked**: Horizontal bars (30→50→60→60→50→30)
3. **Grid**: Small rectangles in grid pattern

### mn+ Signature (3 Random Styles):

1. **Solid**: Bold letter forms
2. **Stacked**: Horizontal striped letters
3. **Outlined**: Double-line architectural style

**Every generation = Different combination!**

## 📁 File Management

**Tracked images** (kept):

- Current 2 images listed in `assets/.image_tracker.json`

**Untracked images** (deleted):

- Anything else gets cleaned up automatically

## 🚀 Next Steps

1. **For GitHub Actions** (automatic updates):
   - Already configured in your script
   - Set `GITHUB_TOKEN` environment variable
   - Run on schedule (e.g., every 12 hours)
   - Images regenerate only when 2 days pass

2. **Test locally**:

   ```bash
   export GITHUB_TOKEN=your_token
   python update_readme.py
   ```

3. **Force new images anytime**:
   ```bash
   python force_regenerate.py
   ```

## 🎨 What Makes Each Generation Unique

- **Random theme** (balloon or mn+)
- **Random style** (3 variations per theme)
- **Random seed** (based on timestamp)
- **Random placement** of decorative rectangles
- **Random colors** from Bauhaus palette
- **Random variations in sizes** within symmetry rules

**Result**: No two generations will look exactly the same! 🎉

## 📊 Files in This System

| File                         | Purpose                                  |
| ---------------------------- | ---------------------------------------- |
| `bauhaus_generator.py`       | Generates rectangle-based Bauhaus images |
| `image_tracker.py`           | Manages 2-day rotation & cleanup         |
| `update_readme.py`           | Main script (updates README + generates) |
| `force_regenerate.py`        | Manual regeneration for testing          |
| `assets/.image_tracker.json` | Tracks current images & timestamp        |
| `assets/*.png`               | Current active images (2 files)          |

---

**System is READY!** Images will rotate automatically every 2 days with new variations each time. 🎯
