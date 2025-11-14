from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional, Iterable


# ========== Domain models ==========

@dataclass
class Person:
    hoTen: str
    diaChi: str
    soDienThoai: str
    email: str
    ngaySinh: date

    # Giữ vài "getter/setter" theo UML để tương thích (không bắt buộc trong Python)
    def getHoTen(self) -> str: return self.hoTen
    def setHoTen(self, ten: str) -> None: self.hoTen = ten
    def getDiaChi(self) -> str: return self.diaChi
    def setDiaChi(self, diachi: str) -> None: self.diaChi = diachi
    def getSoDienThoai(self) -> str: return self.soDienThoai
    def setSoDienThoai(self, sdt: str) -> None: self.soDienThoai = sdt
    def getEmail(self) -> str: return self.email
    def setEmail(self, e: str) -> None: self.email = e
    def getNgaySinh(self) -> date: return self.ngaySinh
    def setNgaySinh(self, ngay: date) -> None: self.ngaySinh = ngay


@dataclass
class Lop:
    maLop: str
    tenLop: str
    khoa: str
    _sinhViens: Dict[str, "SinhVien"] = field(default_factory=dict, repr=False)

    # Theo UML
    def getMaLop(self) -> str: return self.maLop
    def setMaLop(self, malop: str) -> None: self.maLop = malop
    def getTenLop(self) -> str: return self.tenLop
    def setTenLop(self, ten: str) -> None: self.tenLop = ten
    def getKhoa(self) -> str: return self.khoa
    def setKhoa(self, k: str) -> None: self.khoa = k
    def getSiSo(self) -> int: return len(self._sinhViens)

    # Quản lý SV trong lớp
    def themSinhVien(self, sv: "SinhVien") -> None:
        self._sinhViens[sv.maSinhVien] = sv
        sv.lop = self.maLop

    def xoaSinhVien(self, maSV: str) -> None:
        self._sinhViens.pop(maSV, None)

    def layDanhSachSinhVien(self) -> List["SinhVien"]:
        return list(self._sinhViens.values())


@dataclass
class MonHoc:
    maMonHoc: str
    tenMonHoc: str
    soTinChi: int
    moTa: str = ""

    # Theo UML
    def getMaMonHoc(self) -> str: return self.maMonHoc
    def setMaMonHoc(self, maMH: str) -> None: self.maMonHoc = maMH
    def getTenMonHoc(self) -> str: return self.tenMonHoc
    def setTenMonHoc(self, ten: str) -> None: self.tenMonHoc = ten
    def getSoTinChi(self) -> int: return self.soTinChi
    def setSoTinChi(self, tin: int) -> None: self.soTinChi = tin
    def getMoTa(self) -> str: return self.moTa
    def setMoTa(self, mota: str) -> None: self.moTa = mota


@dataclass
class Diem:
    maSinhVien: str
    maMonHoc: str
    diemGiuaKy: float = 0.0
    diemCuoiKy: float = 0.0
    diemTongKet: Optional(float) = None
    ngayThi: Optional[date] = None

    def setDiemGiuaKy(self, diem: float) -> None: self.diemGiuaKy = diem
    def setDiemCuoiKy(self, diem: float) -> None: self.diemCuoiKy = diem
    def setNgayThi(self, ngay: date) -> None: self.ngayThi = ngay

    # Theo UML: có phương thức tính tổng kết; mặc định 40% GK + 60% CK
    def tinhDiemTongKet(self, w_gk: float = 0.4, w_ck: float = 0.6) -> float:
        self.diemTongKet = round(self.diemGiuaKy * w_gk + self.diemCuoiKy * w_ck, 2)
        return self.diemTongKet or 0.0

    def getDiemTongKet(self) -> float:
        return self.diemTongKet if self.diemTongKet is not None else self.tinhDiemTongKet()


@dataclass
class SinhVien(Person):
    maSinhVien: str
    lop: Optional[str] = None   # lưu maLop cho gọn (có thể tham chiếu đối tượng Lop nếu bạn muốn)
    khoa: str = ""
    namNhapHoc: int = 0
    trangThai: str = "Đang học"

    # Điểm trung bình quy đổi theo tín chỉ (tính qua QuanLySinhVien)
    def hienThiThongTin(self) -> str:
        return f"[{self.maSinhVien}] {self.hoTen} - Lớp: {self.lop or 'N/A'} - Khoa: {self.khoa} - Trạng thái: {self.trangThai}"


# ========== Service layer ==========

class QuanLySinhVien:
    """
    Lớp quản lý bộ nhớ trong cho:
      - danhSachSinhVien: maSV -> SinhVien
      - danhSachMonHoc:   maMH -> MonHoc
      - danhSachLop:      maLop -> Lop
      - bangDiem:         (maSV, maMH) -> Diem
    """
    def __init__(self) -> None:
        self.danhSachSinhVien: Dict[str, SinhVien] = {}
        self.danhSachMonHoc: Dict[str, MonHoc] = {}
        self.danhSachLop: Dict[str, Lop] = {}
        self.bangDiem: Dict[tuple[str, str], Diem] = {}

    # ----- SinhVien -----
    def themSinhVien(self, sv: SinhVien) -> None:
        self.danhSachSinhVien[sv.maSinhVien] = sv
        if sv.lop and sv.lop in self.danhSachLop:
            self.danhSachLop[sv.lop].themSinhVien(sv)

    def xoaSinhVien(self, maSV: str) -> None:
        sv = self.danhSachSinhVien.pop(maSV, None)
        if sv and sv.lop and sv.lop in self.danhSachLop:
            self.danhSachLop[sv.lop].xoaSinhVien(maSV)
        # xóa cả điểm liên quan
        for key in [k for k in self.bangDiem if k[0] == maSV]:
            self.bangDiem.pop(key, None)

    def suaThongTinSinhVien(self, maSV: str, **updates) -> Optional[SinhVien]:
        sv = self.danhSachSinhVien.get(maSV)
        if not sv:
            return None
        for k, v in updates.items():
            if hasattr(sv, k):
                setattr(sv, k, v)
        return sv

    def timSinhVienTheoMa(self, maSV: str) -> Optional[SinhVien]:
        return self.danhSachSinhVien.get(maSV)

    def timSinhVienTheoTen(self, ten: str) -> List[SinhVien]:
        ten = ten.lower().strip()
        return [sv for sv in self.danhSachSinhVien.values() if ten in sv.hoTen.lower()]

    def layDanhSachSinhVien(self) -> List[SinhVien]:
        return list(self.danhSachSinhVien.values())

    # ----- Lop -----
    def themLop(self, lop: Lop) -> None:
        self.danhSachLop[lop.maLop] = lop

    def xoaLop(self, maLop: str) -> None:
        self.danhSachLop.pop(maLop, None)

    def layDanhSachLop(self) -> List[Lop]:
        return list(self.danhSachLop.values())

    # ----- MonHoc -----
    def themMonHoc(self, mh: MonHoc) -> None:
        self.danhSachMonHoc[mh.maMonHoc] = mh

    def xoaMonHoc(self, maMH: str) -> None:
        self.danhSachMonHoc.pop(maMH, None)
        for key in [k for k in self.bangDiem if k[1] == maMH]:
            self.bangDiem.pop(key, None)

    def layDanhSachMonHoc(self) -> List[MonHoc]:
        return list(self.danhSachMonHoc.values())

    # ----- Điểm -----
    def nhapDiem(self, maSV: str, maMH: str, diem: Diem) -> bool:
        if maSV not in self.danhSachSinhVien or maMH not in self.danhSachMonHoc:
            return False
        diem.maSinhVien = maSV
        diem.maMonHoc = maMH
        diem.tinhDiemTongKet()
        self.bangDiem[(maSV, maMH)] = diem
        return True

    def xemBangDiem(self, maSV: str) -> List[Diem]:
        return [d for (sv, _), d in self.bangDiem.items() if sv == maSV]

    def tinhDiemTrungBinh(self, maSV: str) -> float:
        """Tính ĐTB theo tín chỉ (mặc định): sum(điểm_tk * tín_chỉ) / sum(tín_chỉ)"""
        diems = self.xemBangDiem(maSV)
        if not diems:
            return 0.0
        tong_tc = 0
        tong_diem = 0.0
        for d in diems:
            mh = self.danhSachMonHoc.get(d.maMonHoc)
            if not mh:
                continue
            tc = mh.soTinChi
            tong_tc += tc
            tong_diem += d.getDiemTongKet() * tc
        return round(tong_diem / tong_tc, 2) if tong_tc > 0 else 0.0


# ========== Ví dụ sử dụng tối thiểu ==========
if __name__ == "__main__":
    ql = QuanLySinhVien()

    # Tạo lớp & môn
    ql.themLop(Lop(maLop="DHKTPM17A", tenLop="KTPM 17A", khoa="CNTT"))
    ql.themMonHoc(MonHoc(maMonHoc="CTDL", tenMonHoc="Cấu trúc dữ liệu", soTinChi=3))
    ql.themMonHoc(MonHoc(maMonHoc="MOB", tenMonHoc="Mobile", soTinChi=2))

    # Thêm sinh viên
    sv = SinhVien(
        maSinhVien="SV001",
        hoTen="Nguyễn Văn A",
        diaChi="Hà Nội",
        soDienThoai="0900000000",
        email="a@example.com",
        ngaySinh=date(2004, 5, 12),
        lop="DHKTPM17A",
        khoa="CNTT",
        namNhapHoc=2022,
    )
    ql.themSinhVien(sv)

    # Nhập điểm
    ql.nhapDiem("SV001", "CTDL", Diem(maSinhVien="", maMonHoc="", diemGiuaKy=7.5, diemCuoiKy=8.5))
    ql.nhapDiem("SV001", "MOB",  Diem(maSinhVien="", maMonHoc="", diemGiuaKy=8.0, diemCuoiKy=7.0))

    # Tính ĐTB
    print(sv.hienThiThongTin())
    print("ĐTB:", ql.tinhDiemTrungBinh("SV001"))
