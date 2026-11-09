#!/usr/bin/env python3
"""Generate and patch the Android platform folder for this project.

The upstream repository ships without android/ (it is git-ignored), so CI
generates a fresh Flutter Android scaffold and then forces the identity we
want:

    applicationId / namespace : com.fitness
    android:label             : 健身记录
    MainActivity package      : com.fitness

It also enables core-library desugaring, which flutter_local_notifications
requires and the stock Flutter template does not enable.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile

APP_ID = "com.fitness"
APP_LABEL = "健身记录"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANDROID = os.path.join(ROOT, "android")
SCAFFOLD = os.path.join(tempfile.gettempdir(), "xw_android_scaffold")
ICON_BACKUP = os.path.join(tempfile.gettempdir(), "xw_icons")


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)


def backup_icons() -> None:
    if os.path.isdir(ICON_BACKUP):
        shutil.rmtree(ICON_BACKUP)
    os.makedirs(ICON_BACKUP, exist_ok=True)
    res = os.path.join(ANDROID, "app", "src", "main", "res")
    if not os.path.isdir(res):
        return
    for name in os.listdir(res):
        if name.startswith("mipmap-"):
            shutil.copytree(os.path.join(res, name), os.path.join(ICON_BACKUP, name))


def restore_icons() -> None:
    res = os.path.join(ANDROID, "app", "src", "main", "res")
    if not os.path.isdir(ICON_BACKUP):
        return
    for name in os.listdir(ICON_BACKUP):
        dst = os.path.join(res, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(ICON_BACKUP, name), dst)


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def patch_gradle() -> None:
    kts = os.path.join(ANDROID, "app", "build.gradle.kts")
    groovy = os.path.join(ANDROID, "app", "build.gradle")

    if os.path.exists(kts):
        path = kts
        text = read(path)
        text = re.sub(r'namespace\s*=\s*"[^"]*"', f'namespace = "{APP_ID}"', text)
        text = re.sub(
            r'applicationId\s*=\s*"[^"]*"', f'applicationId = "{APP_ID}"', text
        )
        if "isCoreLibraryDesugaringEnabled" not in text:
            text = text.replace(
                "compileOptions {",
                "compileOptions {\n        isCoreLibraryDesugaringEnabled = true",
                1,
            )
        if "coreLibraryDesugaring" not in text:
            dep = '    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n'
            if "dependencies {" in text:
                text = text.replace("dependencies {", "dependencies {\n" + dep, 1)
            else:
                text = text.rstrip() + "\n\ndependencies {\n" + dep + "}\n"
        write(path, text)
        print("patched", path)
        return

    if os.path.exists(groovy):
        path = groovy
        text = read(path)
        text = re.sub(r'namespace\s+"[^"]*"', f'namespace "{APP_ID}"', text)
        text = re.sub(r'applicationId\s+"[^"]*"', f'applicationId "{APP_ID}"', text)
        if "coreLibraryDesugaringEnabled" not in text:
            text = re.sub(
                r"(compileOptions\s*\{)",
                r"\1\n        coreLibraryDesugaringEnabled true",
                text,
                count=1,
            )
        if "coreLibraryDesugaring" not in text:
            dep = "    coreLibraryDesugaring 'com.android.tools:desugar_jdk_libs:2.1.4'\n"
            if "dependencies {" in text:
                text = text.replace("dependencies {", "dependencies {\n" + dep, 1)
            else:
                text = text.rstrip() + "\n\ndependencies {\n" + dep + "}\n"
        write(path, text)
        print("patched", path)
        return

    raise SystemExit("no app-level build.gradle(.kts) found")


def patch_manifest() -> None:
    path = os.path.join(ANDROID, "app", "src", "main", "AndroidManifest.xml")
    text = read(path)
    text = re.sub(r'android:label="[^"]*"', f'android:label="{APP_LABEL}"', text)

    permissions = [
        "android.permission.POST_NOTIFICATIONS",
        "android.permission.RECEIVE_BOOT_COMPLETED",
        "android.permission.SCHEDULE_EXACT_ALARM",
    ]
    missing = [p for p in permissions if p not in text]
    if missing:
        lines = "".join(f'\n    <uses-permission android:name="{p}"/>' for p in missing)
        match = re.search(r"<manifest\b[^>]*>", text)
        if not match:
            raise SystemExit("malformed AndroidManifest.xml")
        text = text[: match.end()] + lines + text[match.end():]

    write(path, text)
    print("patched", path)



def patch_main_activity() -> None:
    for base, _dirs, files in os.walk(os.path.join(ANDROID, "app", "src", "main")):
        if "MainActivity.kt" in files:
            path = os.path.join(base, "MainActivity.kt")
            text = read(path)
            text = re.sub(r"^package\s+[\w.]+", f"package {APP_ID}", text, count=1, flags=re.M)
            write(path, text)
            print("patched", path)
            return
    raise SystemExit("MainActivity.kt not found")


def main() -> None:
    if os.path.isdir(SCAFFOLD):
        shutil.rmtree(SCAFFOLD)

    run(
        [
            "flutter",
            "create",
            "--platforms=android",
            "--org",
            "com",
            "--project-name",
            "fitness",
            SCAFFOLD,
        ]
    )

    if os.path.isdir(ANDROID):
        backup_icons()
        shutil.rmtree(ANDROID)
    shutil.copytree(os.path.join(SCAFFOLD, "android"), ANDROID)
    restore_icons()

    patch_gradle()
    patch_manifest()
    patch_main_activity()

    print("Android platform ready: applicationId =", APP_ID, "| label =", APP_LABEL)


if __name__ == "__main__":
    sys.exit(main())
