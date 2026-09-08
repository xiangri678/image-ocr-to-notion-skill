import AppKit
import Foundation
import Vision

let paths = CommandLine.arguments.dropFirst()
guard !paths.isEmpty else {
    fputs("Usage: swift macos_vision_ocr.swift image1 image2 ...\n", stderr)
    exit(2)
}

func loadImage(_ path: String) -> CGImage? {
    guard let image = NSImage(contentsOfFile: path) else { return nil }
    return image.cgImage(forProposedRect: nil, context: nil, hints: nil)
}

func upscale(_ image: CGImage, factor: Int) -> CGImage? {
    let width = image.width * factor
    let height = image.height * factor
    guard let context = CGContext(
        data: nil,
        width: width,
        height: height,
        bitsPerComponent: 8,
        bytesPerRow: width * 4,
        space: CGColorSpace(name: CGColorSpace.sRGB)!,
        bitmapInfo: CGImageAlphaInfo.premultipliedFirst.rawValue
    ) else { return nil }
    context.interpolationQuality = .high
    context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
    return context.makeImage()
}

func recognize(_ path: String) -> String {
    guard var image = loadImage(path) else { return "[ERROR: cannot load \(path)]" }
    if image.width < 400 || image.height < 400, let enlarged = upscale(image, factor: 8) {
        image = enlarged
    }

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en-US"]
    if #available(macOS 13.0, *) {
        request.revision = VNRecognizeTextRequestRevision3
    }

    do {
        try VNImageRequestHandler(cgImage: image, options: [:]).perform([request])
    } catch {
        return "[ERROR: \(error)]"
    }

    let observations = (request.results ?? []).sorted { left, right in
        let delta = abs(left.boundingBox.midY - right.boundingBox.midY)
        return delta > 0.015
            ? left.boundingBox.midY > right.boundingBox.midY
            : left.boundingBox.minX < right.boundingBox.minX
    }
    return observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
}

for path in paths {
    print("===== \((path as NSString).lastPathComponent) =====")
    print(recognize(String(path)))
    print("")
}
