-- Warehouse Management System - Dump Daten
-- Test-Datensatz für das Lagerverwaltungssystem (Auto-Zubehör)

-- ============================================
-- Users/Staff
-- ============================================
INSERT INTO users (id, username, full_name, email, role, active) VALUES
('U001', 'admin', 'Administrator', 'admin@autozubehoer.de', 'admin', 1),
('U002', 'lagerleiter', 'Hans Mueller', 'hans.mueller@autozubehoer.de', 'lagerleiter', 1),
('U003', 'mitarbeiter1', 'Anna Schmidt', 'anna.schmidt@autozubehoer.de', 'mitarbeiter', 1),
('U004', 'mitarbeiter2', 'Klaus Weber', 'klaus.weber@autozubehoer.de', 'mitarbeiter', 1),
('U005', 'viewer', 'Management', 'management@autozubehoer.de', 'viewer', 1);

-- ============================================
-- Warehouse
-- ============================================
INSERT INTO warehouses (id, name, location, created_at) VALUES
('WH001', 'Hauptlager Autozubehör', 'München, Oberbayern', datetime('now'));

-- ============================================
-- Categories
-- ============================================
INSERT INTO categories (id, name, description, created_at) VALUES
('CAT001', 'Reifen', 'Autoreifen - Winter und Sommer', datetime('now')),
('CAT002', 'Öl & Flüssigkeiten', 'Motoröle, Bremsflüssigkeit, Kühlmittel', datetime('now')),
('CAT003', 'Batterien', 'Starterbatterien für verschiedene Fahrzeugtypen', datetime('now')),
('CAT004', 'Bremsen', 'Bremsbeläge, Bremsscheiben und Zubehör', datetime('now')),
('CAT005', 'Licht & Elektrik', 'Lampen, Starterkabel, elektrisches Zubehör', datetime('now')),
('CAT006', 'Scheibenwischer', 'Scheibenreinigungssysteme und Wischer', datetime('now')),
('CAT007', 'Innenraum', 'Fußmatten, Lenkradbezüge, Sitzbezüge', datetime('now')),
('CAT008', 'Werkzeug', 'Wagenheber, Radkreuze, Spezialwerkzeug', datetime('now')),
('CAT009', 'Sonstiges', 'Warndreieck, Verbandkasten, Sicherheitsausrüstung', datetime('now'));

-- ============================================
-- Brands
-- ============================================
INSERT INTO brands (id, name, country, website, created_at) VALUES
('BRAND001', 'Michelin', 'Frankreich', 'www.michelin.de', datetime('now')),
('BRAND002', 'Continental', 'Deutschland', 'www.continental.com', datetime('now')),
('BRAND003', 'Castrol', 'Vereinigtes Königreich', 'www.castrol.com', datetime('now')),
('BRAND004', 'ATE', 'Deutschland', 'www.ate.eu', datetime('now')),
('BRAND005', 'Osram', 'Deutschland', 'www.osram.com', datetime('now')),
('BRAND006', 'Bosch', 'Deutschland', 'www.bosch.com', datetime('now')),
('BRAND007', 'Philips', 'Niederlande', 'www.philips.com', datetime('now')),
('BRAND008', 'Einhell', 'Deutschland', 'www.einhell.com', datetime('now')),
('BRAND009', 'SWF', 'Deutschland', 'www.bosch-swf.com', datetime('now')),
('BRAND010', 'Walser', 'Deutschland', 'www.walser.de', datetime('now')),
('BRAND011', 'Heyner', 'Deutschland', 'www.heyner.de', datetime('now')),
('BRAND012', 'Kunzer', 'Deutschland', 'www.kunzer.de', datetime('now')),
('BRAND013', 'Vigor', 'Deutschland', 'www.vigor.de', datetime('now')),
('BRAND014', 'KS Tools', 'Deutschland', 'www.ks-tools.com', datetime('now')),
('BRAND015', 'Petex', 'Deutschland', 'www.petex.de', datetime('now')),
('BRAND016', 'Leina', 'Deutschland', 'www.leina.de', datetime('now')),
('BRAND017', '3M', 'USA', 'www.3m.com', datetime('now')),
('BRAND018', 'Varta', 'Deutschland', 'www.varta.de', datetime('now')),
('BRAND019', 'Brembo', 'Italien', 'www.brembo.com', datetime('now')),
('BRAND020', 'Glysantin', 'Deutschland', 'www.glysantin.de', datetime('now'));

-- ============================================
-- Products
-- ============================================
INSERT INTO products (id, warehouse_id, sku, name, description, category_id, brand_id, price, quantity, location, min_stock, max_stock, created_at, updated_at, notes) VALUES
-- Reifen
('PROD001', 'WH001', 'MICH-WIN-205-55-R16', 'Winterreifen Michelin 205/55R16', 'Premium Winterreifen für PKW, M+S Kennzeichnung', 'CAT001', 'BRAND001', 89.99, 24, 'A1-01', 5, 50, datetime('now'), datetime('now'), 'Hochwertige Winterreifen'),
('PROD002', 'WH001', 'CONT-SOM-195-65-R15', 'Sommerreifen Continental 195/65R15', 'Hochwertiger Sommerreifen, gute Nasshaftung', 'CAT001', 'BRAND002', 75.50, 18, 'A1-02', 5, 40, datetime('now'), datetime('now'), 'Populäres Modell'),

-- Öl & Flüssigkeiten
('PROD003', 'WH001', 'CAST-EDGE-5W30-5L', 'Motoröl 5W-30 Castrol Edge', 'Vollsynthetisches Motoröl, 5 Liter Kanister', 'CAT002', 'BRAND003', 45.99, 35, 'B2-01', 10, 100, datetime('now'), datetime('now'), 'Bestseller Artikel'),
('PROD004', 'WH001', 'BRE-DOT4-1L', 'Bremsflüssigkeit DOT 4', 'Hochleistungs-Bremsflüssigkeit, 1 Liter', 'CAT002', 'BRAND004', 12.49, 50, 'B2-02', 15, 80, datetime('now'), datetime('now'), NULL),
('PROD005', 'WH001', 'KUEHL-FROST-5L', 'Kühlerfrostschutz -40°C', 'Fertiggemisch, 5 Liter, blau', 'CAT002', 'BRAND020', 18.99, 28, 'B2-03', 8, 60, datetime('now'), datetime('now'), 'Saisonartikel'),

-- Batterien
('PROD006', 'WH001', 'VARTA-12V-60AH', 'Autobatterie 12V 60Ah', 'Starterbatterie für PKW, wartungsfrei', 'CAT003', 'BRAND018', 79.99, 12, 'C3-01', 3, 25, datetime('now'), datetime('now'), NULL),
('PROD007', 'WH001', 'BOSCH-AGM-74AH', 'Autobatterie 12V 74Ah AGM', 'AGM-Technologie, Start-Stop geeignet', 'CAT003', 'BRAND006', 149.99, 8, 'C3-02', 2, 15, datetime('now'), datetime('now'), 'Premium Batterie'),

-- Bremsen
('PROD008', 'WH001', 'ATE-BREM-VW-GOLF7-V', 'Bremsbeläge vorne VW Golf 7', 'Hochwertige Bremsbeläge, Satz für Vorderachse', 'CAT004', 'BRAND004', 34.99, 20, 'D4-01', 5, 40, datetime('now'), datetime('now'), NULL),
('PROD009', 'WH001', 'BREM-SCH-BMW-3ER', 'Bremsscheiben Set BMW 3er', 'Belüftete Bremsscheiben, Paar Vorderachse', 'CAT004', 'BRAND019', 89.99, 6, 'D4-02', 2, 20, datetime('now'), datetime('now'), NULL),

-- Licht & Elektrik
('PROD010', 'WH001', 'OSRAM-H7-55W-2P', 'H7 Halogen-Lampe 12V 55W', 'Standard Abblendlicht Lampe, 2er Pack', 'CAT005', 'BRAND005', 9.99, 100, 'E5-01', 20, 200, datetime('now'), datetime('now'), 'Häufig gekauft'),
('PROD011', 'WH001', 'LED-INNEN-SET', 'LED Innenraumbeleuchtung Set', 'Universal LED Set für Innenraum, weiß', 'CAT005', 'BRAND007', 24.99, 30, 'E5-02', 5, 50, datetime('now'), datetime('now'), NULL),
('PROD012', 'WH001', 'START-KABEL-25MM', 'Starterkabel 25mm² 3,5m', 'Starthilfekabel für PKW und Kleintransporter', 'CAT005', 'BRAND008', 29.99, 15, 'E5-03', 3, 30, datetime('now'), datetime('now'), NULL),

-- Scheibenwischer
('PROD013', 'WH001', 'BOSCH-WISCH-600-450', 'Scheibenwischer Set 600/450mm', 'Universelle Flachbalkenwischer, Paar', 'CAT006', 'BRAND006', 19.99, 40, 'F6-01', 10, 80, datetime('now'), datetime('now'), 'Selling Artikel'),
('PROD014', 'WH001', 'HECK-WISCH-300', 'Heckscheibenwischer 300mm', 'Standard Heckwischer für diverse Fahrzeuge', 'CAT006', 'BRAND009', 8.99, 25, 'F6-02', 5, 60, datetime('now'), datetime('now'), NULL),

-- Innenraum
('PROD015', 'WH001', 'FUSS-MAT-UNI-4ER', 'Fußmatten-Set Universal', '4-teiliges Gummi-Fußmatten Set, schwarz', 'CAT007', 'BRAND010', 29.99, 20, 'G7-01', 5, 50, datetime('now'), datetime('now'), NULL),
('PROD016', 'WH001', 'LENK-BEZ-LEDER', 'Lenkradbezug Leder 37-39cm', 'Hochwertiger Leder-Lenkradbezug, universell', 'CAT007', 'BRAND011', 18.99, 15, 'G7-02', 3, 30, datetime('now'), datetime('now'), NULL),

-- Werkzeug
('PROD017', 'WH001', 'WAGEN-HEB-HYD-2T', 'Wagenheber hydraulisch 2t', 'Hydraulischer Rangierwagenheber bis 2 Tonnen', 'CAT008', 'BRAND012', 49.99, 10, 'H8-01', 2, 20, datetime('now'), datetime('now'), NULL),
('PROD018', 'WH001', 'RAD-KREUZ-4ER', 'Radkreuz 17/19/21/23mm', 'Standard Radkreuz für Radwechsel', 'CAT008', 'BRAND013', 14.99, 25, 'H8-02', 5, 50, datetime('now'), datetime('now'), NULL),
('PROD019', 'WH001', 'OEL-FILT-SCHL-SET', 'Ölfilter-Schlüssel Set', '3-teiliges Ölfilter-Schlüssel Set', 'CAT008', 'BRAND014', 22.99, 8, 'H8-03', 2, 20, datetime('now'), datetime('now'), NULL),

-- Sonstiges
('PROD020', 'WH001', 'WARN-DREI-ECE', 'Warndreieck Euro', 'Kompaktes Warndreieck nach ECE R27', 'CAT009', 'BRAND015', 9.99, 45, 'I9-01', 10, 100, datetime('now'), datetime('now'), NULL),
('PROD021', 'WH001', 'VERB-KAST-DIN', 'Verbandskasten DIN 13164', 'KFZ-Verbandkasten nach aktueller Norm', 'CAT009', 'BRAND016', 14.99, 30, 'I9-02', 5, 50, datetime('now'), datetime('now'), NULL),
('PROD022', 'WH001', 'WARN-WEST-GELB', 'Warnweste gelb EN ISO 20471', 'Sicherheitsweste, Einheitsgröße', 'CAT009', 'BRAND017', 3.99, 100, 'I9-03', 20, 200, datetime('now'), datetime('now'), NULL);

-- ============================================
-- Movements (Bestandsbewegungen)
-- ============================================
INSERT INTO movements (id, product_id, warehouse_id, quantity_change, movement_type, reason, performed_by, timestamp) VALUES
('MOV001', 'PROD003', 'WH001', 10, 'IN', 'Nachbestellung eingetroffen', 'admin', '2026-02-15 09:30:00'),
('MOV002', 'PROD001', 'WH001', -4, 'OUT', 'Verkauf an Kunde #1234', 'mitarbeiter1', '2026-02-15 11:45:00'),
('MOV003', 'PROD006', 'WH001', -1, 'OUT', 'Defekt bei Lagerkontrolle festgestellt', 'lagerleiter', '2026-02-16 08:15:00'),
('MOV004', 'PROD010', 'WH001', 50, 'IN', 'Großbestellung eingetroffen', 'admin', '2026-02-16 10:00:00'),
('MOV005', 'PROD013', 'WH001', -5, 'OUT', 'Verkauf Werkstatt XYZ', 'mitarbeiter2', '2026-02-16 14:30:00'),
('MOV006', 'PROD008', 'WH001', 2, 'CORRECTION', 'Inventurkorrektur - tatsächlicher Bestand höher', 'lagerleiter', '2026-02-17 09:00:00'),
('MOV007', 'PROD002', 'WH001', 6, 'IN', 'Nachbestellung Continental', 'admin', '2026-02-17 11:00:00'),
('MOV008', 'PROD004', 'WH001', -3, 'OUT', 'Verkauf Autowerkstatt München', 'mitarbeiter1', '2026-02-17 13:30:00'),
('MOV009', 'PROD005', 'WH001', -2, 'OUT', 'Verkauf privater Kunde', 'mitarbeiter2', '2026-02-17 15:45:00'),
('MOV010', 'PROD007', 'WH001', 3, 'IN', 'Nachbestellung Bosch Batterie', 'admin', '2026-02-18 08:00:00'),
('MOV011', 'PROD011', 'WH001', -8, 'OUT', 'Verkauf TÜV Werkstatt', 'mitarbeiter1', '2026-02-18 10:30:00'),
('MOV012', 'PROD015', 'WH001', 5, 'IN', 'Nachbestellung Fußmatten', 'admin', '2026-02-18 14:00:00'),
('MOV013', 'PROD020', 'WH001', -10, 'OUT', 'Verkauf Autohandel Bernd', 'mitarbeiter2', '2026-02-19 09:15:00'),
('MOV014', 'PROD022', 'WH001', 25, 'IN', 'Großbestellung Warnwesten', 'admin', '2026-02-19 11:30:00');

-- ============================================
-- Inventory Snapshots (tägliche Bestände für Reports)
-- ============================================
INSERT INTO inventory_snapshots (warehouse_id, product_id, quantity, total_value, snapshot_date) VALUES
('WH001', 'PROD001', 24, 2159.76, '2026-02-17'),
('WH001', 'PROD002', 18, 1359.00, '2026-02-17'),
('WH001', 'PROD003', 35, 1609.65, '2026-02-17'),
('WH001', 'PROD004', 50, 624.50, '2026-02-17'),
('WH001', 'PROD005', 28, 531.72, '2026-02-17'),
('WH001', 'PROD006', 12, 959.88, '2026-02-17'),
('WH001', 'PROD007', 8, 1199.92, '2026-02-17'),
('WH001', 'PROD008', 20, 699.80, '2026-02-17'),
('WH001', 'PROD009', 6, 539.94, '2026-02-17'),
('WH001', 'PROD010', 100, 999.00, '2026-02-17'),
('WH001', 'PROD011', 30, 749.70, '2026-02-17'),
('WH001', 'PROD012', 15, 449.85, '2026-02-17'),
('WH001', 'PROD013', 40, 799.60, '2026-02-17'),
('WH001', 'PROD014', 25, 224.75, '2026-02-17'),
('WH001', 'PROD015', 20, 599.80, '2026-02-17'),
('WH001', 'PROD016', 15, 284.85, '2026-02-17'),
('WH001', 'PROD017', 10, 499.90, '2026-02-17'),
('WH001', 'PROD018', 25, 374.75, '2026-02-17'),
('WH001', 'PROD019', 8, 183.92, '2026-02-17'),
('WH001', 'PROD020', 45, 449.55, '2026-02-17'),
('WH001', 'PROD021', 30, 449.70, '2026-02-17'),
('WH001', 'PROD022', 100, 399.00, '2026-02-17'),
-- Snapshot vom nächsten Tag
('WH001', 'PROD001', 20, 1799.80, '2026-02-18'),
('WH001', 'PROD002', 24, 1812.00, '2026-02-18'),
('WH001', 'PROD003', 35, 1609.65, '2026-02-18'),
('WH001', 'PROD004', 47, 586.03, '2026-02-18'),
('WH001', 'PROD005', 26, 493.74, '2026-02-18'),
('WH001', 'PROD006', 14, 1119.86, '2026-02-18'),
('WH001', 'PROD007', 11, 1649.89, '2026-02-18'),
('WH001', 'PROD008', 22, 769.78, '2026-02-18'),
('WH001', 'PROD009', 6, 539.94, '2026-02-18'),
('WH001', 'PROD010', 150, 1498.50, '2026-02-18'),
('WH001', 'PROD011', 22, 549.78, '2026-02-18'),
('WH001', 'PROD012', 15, 449.85, '2026-02-18'),
('WH001', 'PROD013', 35, 699.65, '2026-02-18'),
('WH001', 'PROD014', 25, 224.75, '2026-02-18'),
('WH001', 'PROD015', 25, 749.75, '2026-02-18'),
('WH001', 'PROD016', 15, 284.85, '2026-02-18'),
('WH001', 'PROD017', 10, 499.90, '2026-02-18'),
('WH001', 'PROD018', 25, 374.75, '2026-02-18'),
('WH001', 'PROD019', 8, 183.92, '2026-02-18'),
('WH001', 'PROD020', 35, 349.65, '2026-02-18'),
('WH001', 'PROD021', 30, 449.70, '2026-02-18'),
('WH001', 'PROD022', 125, 498.75, '2026-02-18');
