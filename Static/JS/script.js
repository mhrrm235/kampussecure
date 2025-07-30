// JS interaksi sederhana
document.addEventListener("DOMContentLoaded", () => {
    const scanBtn = document.getElementById("scan-btn");
    if (scanBtn) {
        scanBtn.addEventListener("click", () => {
            scanBtn.disabled = true;
            scanBtn.innerText = "Scanning...";
            setTimeout(() => {
                scanBtn.innerText = "Scan Again";
                scanBtn.disabled = false;
                alert("Scan selesai! Silakan lihat hasilnya di dashboard.");
            }, 2000);
        });
    }
});
