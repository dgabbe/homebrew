cask 'pdfpen-9.2.3' do
  version '9.2.3'
  depends_on macos: ['10.11', '10.12', '10.13']
  sha256 '9c93c5350abd73e474911cf800a44ac197700e800cd6163f4dd4a5ffe5049357'

  url 'https://dl.smilesoftware.com/com.smileonmymac.PDFpen/923.0/1510025892/PDFpen-923.0.zip'
  name 'PDFpen'
  homepage 'https://smilesoftware.com/pdfpen'

  app 'PDFpen.app'
end
