-- Save a shareable Word report at the repository root.
-- Keep the site copy so the HTML page's MS Word download still works.
local outputs = os.getenv("QUARTO_PROJECT_OUTPUT_FILES") or ""

for source in outputs:gmatch("[^\r\n]+") do
  local normalized = source:gsub("\\", "/")
  if normalized:match("/final_report%.docx$") then
    local input = assert(io.open(source, "rb"))
    local content = assert(input:read("*a"))
    assert(input:close())

    local output = assert(io.open("final_report.docx", "wb"))
    assert(output:write(content))
    assert(output:close())

    if os.getenv("QUARTO_PROJECT_SCRIPT_QUIET") ~= "1" then
      print("Word report saved at repository root: final_report.docx")
    end
  end
end
