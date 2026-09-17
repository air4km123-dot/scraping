"use client";

import { useMemo, useState } from "react";
import { Product } from "@/lib/data";

type SortKey = "name" | "price";
type SortDir = "asc" | "desc";

function PriceCell({ product }: { product: Product }) {
  if (!product.priceThb) return <td className="price">—</td>;

  const diff =
    product.priceChange && product.previousPriceThb
      ? Number(product.priceThb) - Number(product.previousPriceThb)
      : null;

  return (
    <td className="price">
      <span className="price-value">{product.priceThb}</span>
      {product.priceChange === "up" && (
        <span className="price-arrow up" title={`เพิ่มขึ้น ${diff} บาท จาก ${product.previousPriceThb}`}>
          ▲ {diff}
        </span>
      )}
      {product.priceChange === "down" && (
        <span className="price-arrow down" title={`ลดลง ${Math.abs(diff ?? 0)} บาท จาก ${product.previousPriceThb}`}>
          ▼ {diff}
        </span>
      )}
    </td>
  );
}

export default function ProductTable({ products }: { products: Product[] }) {
  const [sortKey, setSortKey] = useState<SortKey | null>(null);
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  }

  const sorted = useMemo(() => {
    if (!sortKey) return products;
    const withOrder = [...products];
    withOrder.sort((a, b) => {
      let cmp: number;
      if (sortKey === "name") {
        cmp = (a.name ?? "").localeCompare(b.name ?? "", "th");
      } else {
        const aNum = a.priceThb ? Number(a.priceThb) : null;
        const bNum = b.priceThb ? Number(b.priceThb) : null;
        if (aNum === null && bNum === null) cmp = 0;
        else if (aNum === null) cmp = 1; // no-price rows sort last regardless of direction
        else if (bNum === null) cmp = -1;
        else cmp = aNum - bNum;
      }
      return sortDir === "asc" ? cmp : -cmp;
    });
    return withOrder;
  }, [products, sortKey, sortDir]);

  function indicator(key: SortKey) {
    if (sortKey !== key) return null;
    return <span className="sort-indicator">{sortDir === "asc" ? "▲" : "▼"}</span>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>
            <button type="button" className="sort-btn" onClick={() => toggleSort("name")}>
              Product {indicator("name")}
            </button>
          </th>
          <th>
            <button type="button" className="sort-btn sort-btn-right" onClick={() => toggleSort("price")}>
              Price (THB) {indicator("price")}
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((p) => (
          <tr key={p.sourceUrl}>
            <td>
              <a href={p.sourceUrl} target="_blank" rel="noreferrer">
                {p.name ?? p.sourceUrl}
              </a>
            </td>
            <PriceCell product={p} />
          </tr>
        ))}
      </tbody>
    </table>
  );
}
