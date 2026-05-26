#!/bin/bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage:"
  echo "  bash read_local_pdf.sh pages <pdf-path>"
  echo "  bash read_local_pdf.sh text <pdf-path> [start_page] [end_page]"
  echo "  bash read_local_pdf.sh highlights <pdf-path> [start_page] [end_page]"
  exit 1
fi

MODE="$1"
PDF_PATH="$2"

if [ ! -f "$PDF_PATH" ]; then
  echo "PDF not found: $PDF_PATH" >&2
  exit 1
fi

TMP_DIR="$(mktemp -d /tmp/local-pdf-reader.XXXXXX)"
SRC="$TMP_DIR/read_pdf.m"
BIN="$TMP_DIR/read_pdf"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cat >"$SRC" <<'EOF'
#import <Foundation/Foundation.h>
#import <PDFKit/PDFKit.h>

static NSString *Collapse(NSString *s) {
    if (s == nil) return @"";
    NSMutableString *m = [s mutableCopy];
    [m replaceOccurrencesOfString:@"\r\n" withString:@"\n" options:0 range:NSMakeRange(0, m.length)];
    [m replaceOccurrencesOfString:@"\r" withString:@"\n" options:0 range:NSMakeRange(0, m.length)];
    [m replaceOccurrencesOfString:@"\n" withString:@" " options:0 range:NSMakeRange(0, m.length)];
    while ([m containsString:@"  "]) {
        [m replaceOccurrencesOfString:@"  " withString:@" " options:0 range:NSMakeRange(0, m.length)];
    }
    return [m stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
}

static void PrintUsage(void) {
    printf("Usage:\n");
    printf("  read_pdf pages <pdf-path>\n");
    printf("  read_pdf text <pdf-path> [start_page] [end_page]\n");
    printf("  read_pdf highlights <pdf-path> [start_page] [end_page]\n");
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 3) {
            PrintUsage();
            return 1;
        }

        NSString *mode = [NSString stringWithUTF8String:argv[1]];
        NSString *path = [NSString stringWithUTF8String:argv[2]];
        PDFDocument *doc = [[PDFDocument alloc] initWithURL:[NSURL fileURLWithPath:path]];
        if (doc == nil) {
            fprintf(stderr, "Failed to open PDF: %s\n", path.UTF8String);
            return 1;
        }

        NSInteger startPage = 1;
        NSInteger endPage = doc.pageCount;
        if (argc >= 4) {
            startPage = [[NSString stringWithUTF8String:argv[3]] integerValue];
        }
        if (argc >= 5) {
            endPage = [[NSString stringWithUTF8String:argv[4]] integerValue];
        } else if (argc >= 4 && [mode isEqualToString:@"text"]) {
            endPage = startPage;
        }

        if ([mode isEqualToString:@"pages"]) {
            printf("%ld\n", (long)doc.pageCount);
            return 0;
        }

        if (startPage < 1) startPage = 1;
        if (endPage < 1 || endPage > doc.pageCount) endPage = doc.pageCount;
        if (startPage > endPage) {
            NSInteger tmp = startPage;
            startPage = endPage;
            endPage = tmp;
        }

        if ([mode isEqualToString:@"text"]) {
            for (NSInteger i = startPage; i <= endPage; i++) {
                PDFPage *page = [doc pageAtIndex:i - 1];
                NSString *text = page.string ?: @"";
                printf("===== PAGE %ld =====\n", (long)i);
                printf("%s\n", text.UTF8String);
            }
            return 0;
        }

        if ([mode isEqualToString:@"highlights"]) {
            for (NSInteger i = startPage; i <= endPage; i++) {
                PDFPage *page = [doc pageAtIndex:i - 1];
                NSArray<PDFAnnotation *> *annotations = [page annotations];
                NSInteger highlightIndex = 0;
                BOOL printedPage = NO;
                for (PDFAnnotation *annotation in annotations) {
                    NSString *type = annotation.type ?: @"";
                    if (![type.lowercaseString containsString:@"highlight"]) {
                        continue;
                    }
                    if (!printedPage) {
                        printf("===== PAGE %ld =====\n", (long)i);
                        printedPage = YES;
                    }
                    highlightIndex += 1;
                    NSRect bounds = NSInsetRect(annotation.bounds, -2, -2);
                    PDFSelection *selection = [page selectionForRect:bounds];
                    NSString *text = Collapse(selection.string);
                    printf("H%ld|%s\n", (long)highlightIndex, text.UTF8String);
                }
            }
            return 0;
        }

        fprintf(stderr, "Unknown mode: %s\n", mode.UTF8String);
        PrintUsage();
        return 1;
    }
}
EOF

clang -fobjc-arc -framework Foundation -framework PDFKit "$SRC" -o "$BIN"

ARGS=("$MODE" "$PDF_PATH")
if [ "$#" -ge 3 ]; then
  ARGS+=("$3")
fi
if [ "$#" -ge 4 ]; then
  ARGS+=("$4")
fi

"$BIN" "${ARGS[@]}"
