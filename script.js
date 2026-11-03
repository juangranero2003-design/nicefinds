const AMAZON_TAG = "visit0fb-20";
const PIN_LOG_URL = "pins/log.csv";

const boardSections = Array.from(document.querySelectorAll(".board-section[data-board]"));
const productGridByBoard = new Map(
  boardSections.map((section) => [section.dataset.board, section.querySelector(".product-grid")]),
);

function parseCSV(csvText) {
  const text = csvText.replace(/^\uFEFF/, "");
  const rows = [];
  let row = [];
  let field = "";
  let insideQuotes = false;

  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];

    if (insideQuotes) {
      if (character === '"' && text[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (character === '"') {
        insideQuotes = false;
      } else {
        field += character;
      }
      continue;
    }

    if (character === '"' && field.length === 0) {
      insideQuotes = true;
    } else if (character === ",") {
      row.push(field);
      field = "";
    } else if (character === "\n" || character === "\r") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
      if (character === "\r" && text[index + 1] === "\n") index += 1;
    } else {
      field += character;
    }
  }

  if (insideQuotes) throw new Error("The product log contains an unclosed quoted field.");
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  return rows;
}

function readProducts(csvText) {
  const [headers, ...records] = parseCSV(csvText);
  if (!headers) throw new Error("The product log is empty.");

  const column = Object.fromEntries(headers.map((header, index) => [header.trim(), index]));
  const requiredColumns = ["date", "file", "asin", "board", "title"];
  if (requiredColumns.some((name) => column[name] === undefined)) {
    throw new Error("The product log is missing a required column.");
  }

  return records
    .filter((record) => record.some((value) => value.trim() !== ""))
    .map((record) => ({
      date: (record[column.date] ?? "").trim(),
      file: (record[column.file] ?? "").trim(),
      asin: (record[column.asin] ?? "").trim().toUpperCase(),
      board: (record[column.board] ?? "").trim(),
      title: (record[column.title] ?? "").trim(),
    }))
    .filter((product) =>
      /^[A-Za-z0-9_-]+$/.test(product.file)
      && /^[A-Z0-9]{10}$/.test(product.asin)
      && product.board.length > 0
      && product.title.length > 0,
    )
    .sort((first, second) => second.date.localeCompare(first.date));
}

function createProductCard(product) {
  const card = document.createElement("article");
  card.className = "product-card";

  const image = document.createElement("img");
  image.className = "product-image";
  image.src = `pins/${encodeURIComponent(product.file)}.png`;
  image.alt = product.title;
  image.width = 1000;
  image.height = 1500;
  image.loading = "lazy";
  // If the pin image is missing, hide the card instead of showing a broken image.
  image.addEventListener("error", () => {
    console.warn(`Missing pin image for "${product.title}": ${image.src}`);
    card.remove();
  });

  const details = document.createElement("div");
  details.className = "product-details";

  const title = document.createElement("h3");
  title.className = "product-title";
  title.textContent = product.title;

  const link = document.createElement("a");
  link.className = "amazon-link";
  link.href = `https://www.amazon.com/dp/${encodeURIComponent(product.asin)}?tag=${AMAZON_TAG}`;
  link.target = "_blank";
  // "sponsored" tells search engines this is an affiliate link.
  link.rel = "sponsored noopener noreferrer";
  link.textContent = "View on Amazon";

  details.append(title, link);
  card.append(image, details);
  return card;
}

function showMessage(grid, message, className) {
  const paragraph = document.createElement("p");
  paragraph.className = className;
  paragraph.textContent = message;
  grid.replaceChildren(paragraph);
}

function renderProducts(products) {
  // Warn about rows whose board name doesn't match any section on the page.
  for (const product of products) {
    if (!productGridByBoard.has(product.board)) {
      console.warn(`Unknown board "${product.board}" for "${product.title}". Check pins/log.csv.`);
    }
  }

  for (const [board, grid] of productGridByBoard) {
    const boardProducts = products.filter((product) => product.board === board);
    if (boardProducts.length === 0) {
      showMessage(grid, "No finds here just yet. Check back soon.", "empty-message");
      continue;
    }

    grid.replaceChildren(...boardProducts.map(createProductCard));
  }
}

async function loadProducts() {
  try {
    // "no-cache" makes the browser check for a fresh log.csv, so new pins show up right away.
    const response = await fetch(PIN_LOG_URL, { cache: "no-cache" });
    if (!response.ok) throw new Error(`Could not load the product log (${response.status}).`);
    renderProducts(readProducts(await response.text()));
  } catch (error) {
    console.error("Could not load products:", error);
    for (const grid of productGridByBoard.values()) {
      showMessage(grid, "Products could not be loaded. Please try again later.", "error-message");
    }
  }
}

loadProducts();