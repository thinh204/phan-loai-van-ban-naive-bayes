import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const here = path.dirname(fileURLToPath(import.meta.url));
const workspaceDir = path.resolve(here, "..");
const skillDir = process.env.SKILL_DIR;
const runtimePython = process.env.RUNTIME_PYTHON;
if (!path.isAbsolute(skillDir ?? "") || !path.isAbsolute(runtimePython ?? "")) {
  throw new Error("Set SKILL_DIR and RUNTIME_PYTHON to absolute paths");
}
const tmpDir = path.join(workspaceDir, ".build");
const outputDir = path.join(workspaceDir, "presentation");
await fs.mkdir(tmpDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });
const { applyPresentationChartFont, finalizePresentation } = await import(
  pathToFileURL(path.join(skillDir, "container_tools", "artifact_tool_utils.mjs")).href
);

const metrics = JSON.parse(await fs.readFile(path.join(workspaceDir, "results", "metrics.json"), "utf8"));
const font = "Arial";
const navy = "#142A3B";
const teal = "#007E87";
const muted = "#49616E";
const white = "#FFFFFF";
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });

function textbox(slide, text, left, top, width, height, size = 28, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left, top, width, height },
    fill: "none",
    line: { fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: font,
    fontSize: size,
    bold: opts.bold ?? false,
    color: opts.color ?? navy,
    autoFit: "none",
  };
  return shape;
}

function slide(title, number, notes) {
  const s = deck.slides.add();
  s.background.fill = white;
  textbox(s, title, 72, 42, 1136, 76, 40, { bold: true });
  textbox(s, String(number).padStart(2, "0"), 1164, 658, 44, 32, 17, { color: muted });
  s.speakerNotes.textFrame.setText(notes);
  return s;
}

// 1. Cover
{
  const s = deck.slides.add();
  s.background.fill = navy;
  textbox(s, "PHÂN LOẠI VĂN BẢN", 80, 150, 1100, 90, 56, { bold: true, color: white });
  textbox(s, "bằng Naive Bayes đa thức", 80, 250, 1100, 84, 46, { color: "#B7E8E5" });
  textbox(s, "Môn Trí tuệ nhân tạo  ·  Nhóm 3 thành viên", 82, 555, 1050, 42, 24, { color: white });
  s.speakerNotes.textFrame.setText("Mở bài: giới thiệu mục tiêu là nghiên cứu một thuật toán phân loại văn bản và kiểm chứng bằng thực nghiệm. Thành viên 1 trình bày slide 1–3.");
}

// 2. Problem
{
  const s = slide("Bài toán và dữ liệu", 2,
    "Nguồn: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html. Bốn chủ đề được chọn từ 20 Newsgroups; dữ liệu là tiếng Anh. Thành viên 1 giải thích đầu vào và nhãn.");
  textbox(s, "Đầu vào", 84, 178, 350, 54, 28, { bold: true, color: teal });
  textbox(s, "Nội dung một bài đăng", 84, 236, 460, 55, 30);
  textbox(s, "Đầu ra", 620, 178, 350, 54, 28, { bold: true, color: teal });
  textbox(s, "Một trong bốn chủ đề", 620, 236, 500, 55, 30);
  textbox(s, "Đồ họa máy tính\nBóng chày", 84, 374, 500, 150, 29);
  textbox(s, "Không gian\nChính trị tổng hợp", 620, 374, 500, 150, 29);
  textbox(s, "Dữ liệu: 20 Newsgroups, tập train và test có sẵn", 84, 593, 1060, 42, 23, { color: muted });
}

// 3. Method pipeline
{
  const s = slide("Quy trình phân loại", 3,
    "Tách sẵn train/test. Fit bộ từ vựng và mô hình chỉ trên train; transform/predict trên test. Nguồn: https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html. Thành viên 1 kết thúc tại đây.");
  textbox(s, "1  Văn bản", 84, 185, 520, 66, 34, { bold: true, color: teal });
  textbox(s, "2  Véc-tơ từ", 680, 185, 510, 66, 34, { bold: true, color: teal });
  textbox(s, "3  Naive Bayes", 84, 386, 520, 66, 34, { bold: true, color: teal });
  textbox(s, "4  Nhãn dự đoán", 680, 386, 510, 66, 34, { bold: true, color: teal });
  textbox(s, "Từ ngữ trong bài viết", 84, 252, 500, 74, 25);
  textbox(s, "Bag of Words hoặc TF-IDF", 680, 252, 500, 74, 25);
  textbox(s, "Tính điểm cho từng lớp", 84, 453, 500, 74, 25);
  textbox(s, "Chọn lớp có điểm cao nhất", 680, 453, 500, 74, 25);
  textbox(s, "Fit trên train; test chỉ dùng để đánh giá", 84, 602, 1080, 40, 22, { color: muted });
}

// 4. Features
{
  const s = slide("Hai cách biểu diễn văn bản", 4,
    "Nguồn: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html. Cả hai cách biểu diễn cung cấp đặc trưng cho cùng mô hình MultinomialNB. Thành viên 2 trình bày slide 4–6.");
  textbox(s, "Bag of Words", 84, 190, 470, 55, 34, { bold: true, color: teal });
  textbox(s, "Đếm số lần mỗi từ xuất hiện", 84, 257, 500, 86, 27);
  textbox(s, "“bóng đá bóng” → [2, 1, 0]", 84, 374, 500, 80, 27);
  textbox(s, "TF-IDF", 665, 190, 470, 55, 34, { bold: true, color: teal });
  textbox(s, "Giảm trọng số từ xuất hiện ở nhiều tài liệu", 665, 257, 500, 115, 27);
  textbox(s, "Vẫn giữ véc-tơ không âm cho MNB", 665, 374, 500, 80, 27);
  textbox(s, "Cả hai không giữ thứ tự dài giữa các từ", 84, 565, 1040, 50, 24, { color: muted });
}

// 5. Model
{
  const s = slide("Multinomial Naive Bayes", 5,
    "Nguồn công thức và làm trơn: https://scikit-learn.org/stable/modules/naive_bayes.html. Giải thích giả định độc lập có điều kiện chỉ là xấp xỉ, không có nghĩa từ ngữ độc lập thật. Thành viên 2 trình bày.");
  textbox(s, "P(c | d) ∝ P(d | c) P(c)", 86, 172, 1050, 78, 39, { bold: true, color: teal });
  textbox(s, "score(c, x) = log P(c) + Σᵢ xᵢ log θ(c,i)", 86, 284, 1100, 95, 32);
  textbox(s, "θ(c,i) = [N(c,i) + α] / [N(c) + αV]", 86, 406, 1100, 95, 32);
  textbox(s, "α = 1: làm trơn Laplace để từ chưa thấy không có xác suất bằng 0", 86, 562, 1080, 68, 24, { color: muted });
}

// 6. Toy example
{
  const s = slide("Ví dụ tính tay: “bóng đá mới”", 6,
    "Bốn câu train: thể thao gồm 'bóng đá thắng', 'bóng đá đội'; công nghệ gồm 'máy tính nhanh', 'máy tính mới'. V=8, N mỗi lớp=6, alpha=1. Điểm thể thao=9/5488; công nghệ=2/5488. Đây là ví dụ minh họa, không phải kết quả dữ liệu thật. Thành viên 2 trình bày.");
  textbox(s, "Từ", 85, 184, 250, 52, 26, { bold: true, color: teal });
  textbox(s, "Thể thao", 440, 184, 300, 52, 26, { bold: true, color: teal });
  textbox(s, "Công nghệ", 805, 184, 300, 52, 26, { bold: true, color: teal });
  const rows = [["bóng", "3/14", "1/14"], ["đá", "3/14", "1/14"], ["mới", "1/14", "2/14"]];
  rows.forEach((r, i) => {
    const y = 270 + i * 81;
    textbox(s, r[0], 85, y, 250, 54, 28);
    textbox(s, r[1], 440, y, 300, 54, 28);
    textbox(s, r[2], 805, y, 300, 54, 28);
  });
  textbox(s, "Điểm Thể thao = 9/5488    >    Công nghệ = 2/5488", 85, 554, 1090, 65, 26, { bold: true });
}

// 7. Experiment
{
  const s = slide("Thiết kế thực nghiệm", 7,
    "Nguồn dữ liệu: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html. Tham số và số mẫu lấy từ results/metrics.json. Việc remove metadata theo gợi ý: https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html. Thành viên 3 trình bày slide 7–10.");
  textbox(s, "2.239", 85, 177, 410, 85, 54, { bold: true, color: teal });
  textbox(s, "mẫu train", 85, 265, 430, 50, 26);
  textbox(s, "1.490", 666, 177, 420, 85, 54, { bold: true, color: teal });
  textbox(s, "mẫu test", 666, 265, 430, 50, 26);
  textbox(s, "Cùng MultinomialNB, α = 1", 85, 396, 1090, 56, 30, { bold: true });
  textbox(s, "So sánh CountVectorizer và TfidfVectorizer", 85, 471, 1090, 60, 27);
  textbox(s, "Loại header, chữ ký, trích dẫn trước khi học", 85, 548, 1090, 60, 24, { color: muted });
}

// 8. Results
{
  const s = slide("Kết quả trên tập test", 8,
    "Nguồn: results/metrics.json, tạo bởi src/run_experiment.py với scikit-learn 1.7.2. Accuracy Count 0.8544, TF-IDF 0.8718; macro F1 Count 0.8520, TF-IDF 0.8687. Chênh lệch chỉ áp dụng cho cấu hình này. Thành viên 3 trình bày.");
  const c = s.charts.add("bar", {
    position: { left: 90, top: 180, width: 1060, height: 350 },
    categories: ["Accuracy", "Macro F1"],
    series: [
      { name: "Bag of Words", values: [
        +(metrics.models.count.accuracy * 100).toFixed(2),
        +(metrics.models.count.macro_f1 * 100).toFixed(2),
      ], fill: muted },
      { name: "TF-IDF", values: [
        +(metrics.models.tfidf.accuracy * 100).toFixed(2),
        +(metrics.models.tfidf.macro_f1 * 100).toFixed(2),
      ], fill: teal },
    ],
    barOptions: { direction: "column", grouping: "clustered" },
    hasLegend: true,
    legend: { position: "bottom", textStyle: { fontSize: 20, fill: muted } },
    xAxis: { textStyle: { fontSize: 20, fill: muted } },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 18, fill: navy, bold: true } },
  });
  applyPresentationChartFont(c, { fontFamily: font });
  textbox(s, "Đơn vị: %  ·  TF-IDF cao hơn khoảng 1,7 điểm phần trăm", 91, 575, 1060, 52, 23, { color: muted });
}

// 9. Error analysis
{
  const s = slide("Các cặp chủ đề dễ nhầm", 9,
    "Nguồn: results/confusion_count.csv và results/confusion_tfidf.csv. Space→Politics giảm 62 xuống 14; Politics→Space tăng 15 lên 45. Recall politics giảm 0.900 xuống 0.758. 42 mẫu test rỗng sau lọc. Không diễn giải đây là nguyên nhân duy nhất. Thành viên 3 trình bày.");
  textbox(s, "Không gian → Chính trị", 84, 185, 1000, 60, 30, { bold: true });
  textbox(s, "62 xuống 14", 84, 255, 1000, 66, 42, { color: teal });
  textbox(s, "Chính trị → Không gian", 84, 375, 1000, 60, 30, { bold: true });
  textbox(s, "15 lên 45", 84, 445, 1000, 66, 42, { color: teal });
  textbox(s, "TF-IDF tăng điểm chung nhưng giảm recall của lớp chính trị", 84, 572, 1080, 68, 24, { color: muted });
}

// 10. Conclusion
{
  const s = slide("Kết luận và giới hạn", 10,
    "Tóm tắt: MNB phân loại được bốn chủ đề với macro F1 0.8687 khi dùng TF-IDF. Giới hạn: dữ liệu tiếng Anh, bốn lớp, một tập test, 42 văn bản test rỗng sau lọc. Hướng mở rộng: dữ liệu tiếng Việt có nhãn, validation riêng, thử n-gram. Nguồn đầy đủ trong docs/bao-cao.md. Thành viên 3 kết thúc và mời câu hỏi.");
  textbox(s, "MNB là mô hình đơn giản, dễ giải thích", 84, 180, 1080, 62, 31, { bold: true, color: teal });
  textbox(s, "Macro F1 tốt nhất trong thử nghiệm: 0,8687 với TF-IDF", 84, 275, 1080, 90, 29);
  textbox(s, "Giới hạn: dữ liệu tiếng Anh, bốn lớp, một tập test", 84, 405, 1080, 75, 27);
  textbox(s, "Bước tiếp: dữ liệu tiếng Việt và tập validation riêng", 84, 520, 1080, 75, 27);
}

// The finalizer preserves existing files; each rebuild gets a new output name.
const outputName = process.env.PRESENTATION_OUTPUT_NAME ??
  `phan-loai-van-ban-naive-bayes-${new Date().toISOString().replace(/[:.]/g, "-")}.pptx`;
if (path.basename(outputName) !== outputName || !outputName.endsWith(".pptx")) {
  throw new Error("PRESENTATION_OUTPUT_NAME must be a .pptx filename");
}
const outputPath = path.join(outputDir, outputName);
const stageDir = path.join(workspaceDir, ".codex-finalizer");
await fs.mkdir(stageDir, { recursive: true });
const candidatePath = path.join(stageDir, "candidate.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const result = await finalizePresentation({
  explicitTotalSlideCount: 10,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [8],
  materializeLiteralChartWorkbooks: true,
  workspaceDir,
  candidatePath,
  finalPath: outputPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: [
    "--expected-slide-size-emu", "12192000,6858000",
    "--validate-heading-fit",
  ],
  fontPolicy: { basis: "design", families: [font] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stageDir, `${outputName}.validation.json`),
});
console.log(JSON.stringify({ outputPath, result }, null, 2));
