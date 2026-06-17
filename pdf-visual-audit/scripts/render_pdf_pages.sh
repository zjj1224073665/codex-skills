#!/bin/bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: bash render_pdf_pages.sh <pdf-path> <output-dir> [scale] [start_page] [end_page] [--no-flip]" >&2
  exit 2
fi

PDF_PATH="$1"
OUT_DIR="$2"
SCALE="${3:-4}"
START_PAGE="${4:-1}"
END_PAGE="${5:-0}"
FLIP_VERTICAL=1

for arg in "$@"; do
  if [ "$arg" = "--no-flip" ]; then
    FLIP_VERTICAL=0
  fi
done

if [ ! -f "$PDF_PATH" ]; then
  echo "PDF not found: $PDF_PATH" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

TMP_DIR="$(mktemp -d /tmp/pdf-visual-audit.XXXXXX)"
SRC="$TMP_DIR/render_pdf_pages.m"
BIN="$TMP_DIR/render_pdf_pages"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cat >"$SRC" <<'EOF'
#import <Foundation/Foundation.h>
#import <CoreGraphics/CoreGraphics.h>
#import <ImageIO/ImageIO.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 6) {
            fprintf(stderr, "Usage: render_pdf_pages input.pdf output_dir scale start_page end_page\n");
            return 2;
        }

        NSString *inputPath = [NSString stringWithUTF8String:argv[1]];
        NSString *outputDir = [NSString stringWithUTF8String:argv[2]];
        CGFloat scale = atof(argv[3]);
        NSInteger startPage = [[NSString stringWithUTF8String:argv[4]] integerValue];
        NSInteger endPage = [[NSString stringWithUTF8String:argv[5]] integerValue];

        NSError *error = nil;
        [[NSFileManager defaultManager] createDirectoryAtPath:outputDir
                                  withIntermediateDirectories:YES
                                                   attributes:nil
                                                        error:&error];
        if (error != nil) {
            fprintf(stderr, "Could not create output directory: %s\n", [[error localizedDescription] UTF8String]);
            return 1;
        }

        NSURL *inputURL = [NSURL fileURLWithPath:inputPath];
        CGPDFDocumentRef document = CGPDFDocumentCreateWithURL((CFURLRef)inputURL);
        if (document == NULL) {
            fprintf(stderr, "Could not open PDF: %s\n", [inputPath UTF8String]);
            return 1;
        }

        size_t pageCount = CGPDFDocumentGetNumberOfPages(document);
        if (startPage < 1) startPage = 1;
        if (endPage < 1 || endPage > (NSInteger)pageCount) endPage = (NSInteger)pageCount;
        if (startPage > endPage) {
            NSInteger tmp = startPage;
            startPage = endPage;
            endPage = tmp;
        }

        for (NSInteger pageIndex = startPage; pageIndex <= endPage; pageIndex++) {
            CGPDFPageRef page = CGPDFDocumentGetPage(document, (size_t)pageIndex);
            if (page == NULL) {
                continue;
            }

            CGRect box = CGPDFPageGetBoxRect(page, kCGPDFMediaBox);
            size_t width = (size_t)ceil(CGRectGetWidth(box) * scale);
            size_t height = (size_t)ceil(CGRectGetHeight(box) * scale);

            CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
            CGContextRef context = CGBitmapContextCreate(NULL, width, height, 8, width * 4,
                                                         colorSpace, kCGImageAlphaPremultipliedLast);
            CGColorSpaceRelease(colorSpace);
            if (context == NULL) {
                fprintf(stderr, "Could not create bitmap context for page %ld\n", (long)pageIndex);
                continue;
            }

            CGContextSetRGBFillColor(context, 1.0, 1.0, 1.0, 1.0);
            CGContextFillRect(context, CGRectMake(0, 0, width, height));

            CGContextSaveGState(context);
            CGContextTranslateCTM(context, 0, height);
            CGContextScaleCTM(context, scale, -scale);
            CGContextTranslateCTM(context, -box.origin.x, -box.origin.y);
            CGContextDrawPDFPage(context, page);
            CGContextRestoreGState(context);

            CGImageRef image = CGBitmapContextCreateImage(context);
            CGContextRelease(context);
            if (image == NULL) {
                fprintf(stderr, "Could not create image for page %ld\n", (long)pageIndex);
                continue;
            }

            NSString *fileName = [NSString stringWithFormat:@"page-%02ld.png", (long)pageIndex];
            NSString *outputPath = [outputDir stringByAppendingPathComponent:fileName];
            NSURL *outputURL = [NSURL fileURLWithPath:outputPath];

            CGImageDestinationRef destination = CGImageDestinationCreateWithURL((CFURLRef)outputURL,
                                                                               CFSTR("public.png"),
                                                                               1,
                                                                               NULL);
            if (destination == NULL) {
                fprintf(stderr, "Could not create PNG destination for page %ld\n", (long)pageIndex);
                CGImageRelease(image);
                continue;
            }
            CGImageDestinationAddImage(destination, image, NULL);
            if (!CGImageDestinationFinalize(destination)) {
                fprintf(stderr, "Could not write PNG for page %ld\n", (long)pageIndex);
            }
            CFRelease(destination);
            CGImageRelease(image);
        }

        CGPDFDocumentRelease(document);
    }
    return 0;
}
EOF

clang -framework Foundation -framework CoreGraphics -framework ImageIO "$SRC" -o "$BIN"
"$BIN" "$PDF_PATH" "$OUT_DIR" "$SCALE" "$START_PAGE" "$END_PAGE"

if [ "$FLIP_VERTICAL" -eq 1 ]; then
  for png in "$OUT_DIR"/page-*.png; do
    [ -e "$png" ] || continue
    sips -f vertical "$png" >/dev/null
  done
fi

echo "Rendered pages to: $OUT_DIR"
