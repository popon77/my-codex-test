import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QInputDialog, QToolButton, 
    QMessageBox, QLineEdit, QTextEdit, QScrollArea, QSpinBox, QComboBox,
    QGroupBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import os

class CollapsibleSection(QWidget):
    """折りたたみ可能なセクション"""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.toggle_button = QToolButton()
        self.toggle_button.setText(f"▶ {title}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("""
            QToolButton {
                border: none;
                background: #f5f5f5;
                padding: 8px;
                text-align: left;
                font-weight: bold;
                border-radius: 3px;
            }
            QToolButton:hover {
                background: #e8e8e8;
            }
            QToolButton:checked {
                background: #d0d0d0;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_content)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 5, 10, 10)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_area)
        
        self.content_area.hide()
        self.title = title

    def toggle_content(self):
        if self.toggle_button.isChecked():
            self.content_area.show()
            self.toggle_button.setText(f"▼ {self.title}")
        else:
            self.content_area.hide()
            self.toggle_button.setText(f"▶ {self.title}")

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

class SimpleTeamRow(QWidget):
    """簡易編成表示行"""
    def __init__(self, row_id, parent=None):
        super().__init__(parent)
        self.row_id = row_id
        self.parent_widget = parent
        self.character_detail_widgets = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)

        # 編成行全体を囲むフレーム
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                border-radius: 8px;
                background: #f9f9f9;
            }
        """)
        main_frame_layout = QVBoxLayout(main_frame)
        main_frame_layout.setContentsMargins(15, 15, 15, 15)
        main_frame_layout.setSpacing(10)

        # メイン行（キャラ編成とスコア）
        main_layout = QHBoxLayout()
        main_layout.setSpacing(12)

        # キャラ編成（4人分の簡易入力）
        self.character_edits = []
        for i in range(4):
            char_frame = QFrame()
            char_frame.setMinimumHeight(120)  # 最小高さに変更（固定→最小）
            char_frame.setMinimumWidth(140)  # 最小幅を設定
            char_frame.setStyleSheet("""
                QFrame { 
                    border: 2px solid #bbb; 
                    border-radius: 6px; 
                    background: #ffffff; 
                }
            """)
            char_layout = QVBoxLayout(char_frame)
            char_layout.setContentsMargins(8, 8, 8, 8)
            char_layout.setSpacing(6)

            # キャラクター番号ラベル
            char_label = QLabel(f"{i+1}人目")
            char_label.setFixedHeight(20)
            char_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    font-weight: bold;
                    color: #666;
                    background: #f0f0f0;
                    padding: 3px 6px;
                    border-radius: 3px;
                }
            """)
            char_layout.addWidget(char_label)

            # 簡易情報行
            simple_layout = QHBoxLayout()
            simple_layout.setSpacing(4)

            # キャラ名
            char_edit = QLineEdit()
            char_edit.setPlaceholderText(f"キャラ名")
            char_edit.setFixedHeight(24)
            char_edit.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ccc; 
                    background: #fafafa; 
                    font-size: 11px;
                    padding: 4px 6px;
                    border-radius: 3px;
                }
                QLineEdit:focus {
                    border: 2px solid #4a90e2;
                    background: #ffffff;
                }
            """)
            simple_layout.addWidget(char_edit)

            # E（凸数）
            e_label = QLabel("E")
            e_label.setFixedSize(15, 24)
            e_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
            simple_layout.addWidget(e_label)
            
            e_spin = QSpinBox()
            e_spin.setRange(0, 6)
            e_spin.setFixedSize(40, 24)
            e_spin.setStyleSheet("""
                QSpinBox {
                    border: 1px solid #ccc; 
                    background: #fafafa; 
                    font-size: 11px;
                    padding: 3px;
                    border-radius: 3px;
                }
                QSpinBox:focus {
                    border: 2px solid #4a90e2;
                    background: #ffffff;
                }
            """)
            simple_layout.addWidget(e_spin)

            # S（光円錐重畳）
            s_label = QLabel("S")
            s_label.setFixedSize(15, 24)
            s_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
            simple_layout.addWidget(s_label)
            
            s_spin = QSpinBox()
            s_spin.setRange(1, 5)
            s_spin.setValue(1)
            s_spin.setFixedSize(40, 24)
            s_spin.setStyleSheet("""
                QSpinBox {
                    border: 1px solid #ccc; 
                    background: #fafafa; 
                    font-size: 11px;
                    padding: 3px;
                    border-radius: 3px;
                }
                QSpinBox:focus {
                    border: 2px solid #4a90e2;
                    background: #ffffff;
                }
            """)
            simple_layout.addWidget(s_spin)

            # 詳細表示ボタン
            detail_btn = QPushButton("▼")
            detail_btn.setCheckable(True)
            detail_btn.setFixedSize(24, 24)
            detail_btn.setStyleSheet("""
                QPushButton {
                    font-size: 10px;
                    padding: 4px;
                    background: #e8e8e8;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #d8d8d8;
                }
                QPushButton:checked {
                    background: #d0d0d0;
                    color: #333;
                }
            """)
            detail_btn.clicked.connect(lambda checked, idx=i: self.toggle_character_detail(idx, checked))
            
            # 入力フィールドの変更を監視してリアルタイム保存
            char_edit.textChanged.connect(self.save_data_delayed)
            e_spin.valueChanged.connect(self.save_data_delayed)
            s_spin.valueChanged.connect(self.save_data_delayed)
            simple_layout.addWidget(detail_btn)

            char_layout.addLayout(simple_layout)

            # 詳細エリア（初期は非表示）
            detail_widget = self.create_character_detail_widget(i)
            detail_widget.hide()
            char_layout.addWidget(detail_widget)

            main_layout.addWidget(char_frame)
            self.character_edits.append({
                'name': char_edit,
                'eidolon': e_spin,
                'superimpose': s_spin,
                'detail_btn': detail_btn,
                'detail_widget': detail_widget
            })
            self.character_detail_widgets.append(detail_widget)

        # スコア入力
        score_frame = QFrame()
        score_frame.setMinimumHeight(120)  # キャラフレームと同じ最小高さ
        score_frame.setFixedWidth(120)
        score_frame.setStyleSheet("""
            QFrame { 
                border: 2px solid #4a90e2; 
                border-radius: 6px; 
                background: #f0f8ff;
            }
        """)
        score_layout = QVBoxLayout(score_frame)
        score_layout.setContentsMargins(10, 8, 10, 8)
        score_layout.setSpacing(4)
        
        score_title = QLabel("スコア")
        score_title.setFixedHeight(20)
        score_title.setStyleSheet("""
            QLabel {
                font-size: 12px; 
                color: #4a90e2; 
                font-weight: bold;
                background: #e6f3ff;
                padding: 3px 6px;
                border-radius: 3px;
                text-align: center;
            }
        """)
        score_layout.addWidget(score_title)
        
        self.score_edit = QLineEdit()
        self.score_edit.setPlaceholderText("30000")
        self.score_edit.setFixedHeight(30)
        self.score_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #4a90e2; 
                background: #ffffff; 
                font-size: 14px; 
                font-weight: bold;
                padding: 6px 8px;
                border-radius: 4px;
                text-align: center;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                background: #f8fcff;
            }
        """)
        score_layout.addWidget(self.score_edit)
        
        main_layout.addWidget(score_frame)

        # 削除ボタン
        delete_btn = QToolButton()
        delete_btn.setText("×")
        delete_btn.setFixedSize(32, 32)
        delete_btn.setStyleSheet("""
            QToolButton {
                color: #d32f2f;
                background: #ffebee;
                border: 2px solid #f8bbd9;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }
            QToolButton:hover {
                color: #b71c1c;
                background: #ffcdd2;
                border-color: #f06292;
            }
        """)
        delete_btn.clicked.connect(self.delete_row)
        main_layout.addWidget(delete_btn)

        # スコア入力の変更も監視
        self.score_edit.textChanged.connect(self.save_data_delayed)
        
        main_frame_layout.addLayout(main_layout)
        layout.addWidget(main_frame)

    def create_character_detail_widget(self, char_index):
        """キャラクター詳細ウィジェット作成"""
        detail_widget = QWidget()
        detail_widget.setStyleSheet("""
            QWidget {
                background: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 5px;
            }
        """)
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(8, 8, 8, 8)
        detail_layout.setSpacing(6)
        
        # レベル・光円錐
        info_layout = QGridLayout()
        
        # レベル
        info_layout.addWidget(QLabel("Lv:"), 0, 0)
        level_spin = QSpinBox()
        level_spin.setRange(1, 80)
        level_spin.setValue(80)
        level_spin.setMinimumWidth(60)
        level_spin.setStyleSheet("""
            QSpinBox {
                font-size: 10px; 
                padding: 4px; 
                border: 1px solid #ccc;
                border-radius: 3px;
                background: #ffffff;
            }
        """)
        info_layout.addWidget(level_spin, 0, 1)
        
        # 光円錐名
        info_layout.addWidget(QLabel("光円錐:"), 1, 0)
        lightcone_edit = QLineEdit()
        lightcone_edit.setPlaceholderText("光円錐名")
        lightcone_edit.setStyleSheet("""
            QLineEdit {
                font-size: 10px; 
                padding: 5px; 
                border: 1px solid #ccc; 
                border-radius: 3px;
                background: #ffffff;
            }
        """)
        info_layout.addWidget(lightcone_edit, 1, 1, 1, 2)
        
        detail_layout.addLayout(info_layout)
        
        # 遺物メイン効果（簡易版）
        relic_layout = QGridLayout()
        relic_parts = ["胴", "脚", "縄", "球"]
        main_stat_combos = {}
        
        for i, part in enumerate(relic_parts):
            relic_layout.addWidget(QLabel(f"{part}:"), i//2, (i%2)*2)
            combo = QComboBox()
            combo.addItems(["HP%", "攻撃%", "防御%", "会心率", "会心DMG", "撃破", "回復効率", "属性DMG"])
            combo.setStyleSheet("""
                QComboBox {
                    font-size: 9px; 
                    padding: 3px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    background: #ffffff;
                    min-width: 80px;
                }
            """)
            relic_layout.addWidget(combo, i//2, (i%2)*2+1)
            main_stat_combos[part] = combo
        
        detail_layout.addLayout(relic_layout)
        
        # メモ欄
        memo_edit = QTextEdit()
        memo_edit.setMaximumHeight(50)
        memo_edit.setPlaceholderText("セット効果、サブ効果など...")
        memo_edit.setStyleSheet("""
            QTextEdit {
                font-size: 9px; 
                padding: 5px; 
                border: 1px solid #ccc; 
                border-radius: 3px;
                background: #ffffff;
            }
        """)
        detail_layout.addWidget(memo_edit)
        
        # ウィジェット情報を保存
        detail_widget.level_spin = level_spin
        detail_widget.lightcone_edit = lightcone_edit
        detail_widget.main_stat_combos = main_stat_combos
        detail_widget.memo_edit = memo_edit
        
        # 詳細入力フィールドの変更も監視
        level_spin.valueChanged.connect(self.save_data_delayed)
        lightcone_edit.textChanged.connect(self.save_data_delayed)
        memo_edit.textChanged.connect(self.save_data_delayed)
        for combo in main_stat_combos.values():
            combo.currentTextChanged.connect(self.save_data_delayed)
        
        return detail_widget

    def save_data_delayed(self):
        """データ保存を遅延実行（リアルタイム保存用）"""
        if hasattr(self.parent_widget, 'save_data_delayed'):
            self.parent_widget.save_data_delayed()

    def toggle_character_detail(self, char_index, show):
        """キャラクター詳細の表示/非表示を切り替え"""
        detail_widget = self.character_edits[char_index]['detail_widget']
        detail_btn = self.character_edits[char_index]['detail_btn']
        
        if show:
            detail_widget.show()
            detail_btn.setText("▲")
            # 親フレームの高さを動的に調整
            self.adjustSize()
        else:
            detail_widget.hide()
            detail_btn.setText("▼")
            # 親フレームの高さを動的に調整
            self.adjustSize()
        
        # 詳細表示状態の変更を保存
        self.save_data_delayed()

    def delete_row(self):
        """行を削除"""
        if hasattr(self.parent_widget, 'delete_team_row'):
            self.parent_widget.delete_team_row(self.row_id)

    def get_simple_data(self):
        """簡易データを取得"""
        characters = []
        for i, char_edit in enumerate(self.character_edits):
            detail_widget = self.character_detail_widgets[i]
            
            char_data = {
                'name': char_edit['name'].text(),
                'eidolon': char_edit['eidolon'].value(),
                'superimpose': char_edit['superimpose'].value(),
                'level': detail_widget.level_spin.value(),
                'lightcone': detail_widget.lightcone_edit.text(),
                'main_stats': {part: combo.currentText() for part, combo in detail_widget.main_stat_combos.items()},
                'memo': detail_widget.memo_edit.toPlainText(),
                'detail_shown': char_edit['detail_btn'].isChecked()
            }
            characters.append(char_data)
        
        return {
            'characters': characters,
            'score': self.score_edit.text()
        }

    def set_simple_data(self, data):
        """簡易データを設定"""
        if not data:
            return
        
        characters = data.get('characters', [])
        for i, char_edit in enumerate(self.character_edits):
            if i < len(characters):
                char_data = characters[i]
                char_edit['name'].setText(char_data.get('name', ''))
                char_edit['eidolon'].setValue(char_data.get('eidolon', 0))
                char_edit['superimpose'].setValue(char_data.get('superimpose', 1))
                
                # 詳細情報も設定
                detail_widget = self.character_detail_widgets[i]
                detail_widget.level_spin.setValue(char_data.get('level', 80))
                detail_widget.lightcone_edit.setText(char_data.get('lightcone', ''))
                detail_widget.memo_edit.setPlainText(char_data.get('memo', ''))
                
                # メイン効果設定
                main_stats = char_data.get('main_stats', {})
                for part, combo in detail_widget.main_stat_combos.items():
                    if part in main_stats:
                        index = combo.findText(main_stats[part])
                        if index >= 0:
                            combo.setCurrentIndex(index)
                
                # 詳細表示状態の復元
                if char_data.get('detail_shown', False):
                    char_edit['detail_btn'].setChecked(True)
                    self.toggle_character_detail(i, True)
        
        self.score_edit.setText(data.get('score', ''))

class DetailTeamWidget(QWidget):
    """詳細編成ウィジェット"""
    def __init__(self, row_id):
        super().__init__()
        self.row_id = row_id
        self.character_widgets = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # キャラクター詳細（4人分）
        characters_scroll = QScrollArea()
        characters_widget = QWidget()
        characters_layout = QVBoxLayout(characters_widget)

        for i in range(4):
            char_group = QGroupBox(f"キャラクター {i+1}")
            char_group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    margin: 5px 0;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
            """)
            char_layout = QVBoxLayout(char_group)
            
            # 基本情報
            basic_layout = QGridLayout()
            
            # キャラ名
            basic_layout.addWidget(QLabel("キャラ名:"), 0, 0)
            name_edit = QLineEdit()
            name_edit.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
            basic_layout.addWidget(name_edit, 0, 1)
            
            # レベル
            basic_layout.addWidget(QLabel("Lv:"), 0, 2)
            level_spin = QSpinBox()
            level_spin.setRange(1, 80)
            level_spin.setValue(80)
            level_spin.setStyleSheet("padding: 2px; border: 1px solid #ccc;")
            basic_layout.addWidget(level_spin, 0, 3)
            
            # 凸数
            basic_layout.addWidget(QLabel("凸:"), 1, 0)
            eidolon_spin = QSpinBox()
            eidolon_spin.setRange(0, 6)
            eidolon_spin.setStyleSheet("padding: 2px; border: 1px solid #ccc;")
            basic_layout.addWidget(eidolon_spin, 1, 1)
            
            # 光円錐
            basic_layout.addWidget(QLabel("光円錐:"), 1, 2)
            lightcone_edit = QLineEdit()
            lightcone_edit.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
            basic_layout.addWidget(lightcone_edit, 1, 3)
            
            # 光円錐重畳
            basic_layout.addWidget(QLabel("重畳:"), 2, 0)
            superimpose_spin = QSpinBox()
            superimpose_spin.setRange(1, 5)
            superimpose_spin.setValue(1)
            superimpose_spin.setStyleSheet("padding: 2px; border: 1px solid #ccc;")
            basic_layout.addWidget(superimpose_spin, 2, 1)
            
            char_layout.addLayout(basic_layout)
            
            # 遺物詳細（折りたたみ式）
            relic_section = CollapsibleSection("遺物・装備詳細")
            
            # 遺物メイン効果
            main_stats_widget = QWidget()
            main_stats_layout = QGridLayout(main_stats_widget)
            
            relic_parts = ["胴体", "脚部", "連結縄", "次元球"]
            main_stat_combos = {}
            
            for j, part in enumerate(relic_parts):
                main_stats_layout.addWidget(QLabel(f"{part}:"), j, 0)
                combo = QComboBox()
                combo.addItems(["HP%", "攻撃力%", "防御力%", "効果命中", "撃破特効", "エネルギー回復効率", "会心率", "会心ダメージ", "治療量アップ", "属性ダメージ"])
                combo.setStyleSheet("padding: 3px; border: 1px solid #ccc;")
                main_stats_layout.addWidget(combo, j, 1)
                main_stat_combos[part] = combo
            
            relic_section.add_widget(main_stats_widget)
            
            # 遺物セット・サブ効果
            memo_widget = QWidget()
            memo_layout = QVBoxLayout(memo_widget)
            
            memo_layout.addWidget(QLabel("セット効果:"))
            relic_set_edit = QTextEdit()
            relic_set_edit.setMaximumHeight(50)
            relic_set_edit.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
            memo_layout.addWidget(relic_set_edit)
            
            memo_layout.addWidget(QLabel("重要サブ効果:"))
            sub_stats_edit = QTextEdit()
            sub_stats_edit.setMaximumHeight(50)
            sub_stats_edit.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
            memo_layout.addWidget(sub_stats_edit)
            
            relic_section.add_widget(memo_widget)
            char_layout.addWidget(relic_section)
            
            characters_layout.addWidget(char_group)
            
            # ウィジェットを保存
            self.character_widgets.append({
                'name': name_edit,
                'level': level_spin,
                'eidolon': eidolon_spin,
                'lightcone': lightcone_edit,
                'superimpose': superimpose_spin,
                'main_stats': main_stat_combos,
                'relic_set': relic_set_edit,
                'sub_stats': sub_stats_edit
            })

        characters_scroll.setWidget(characters_widget)
        characters_scroll.setWidgetResizable(True)
        layout.addWidget(characters_scroll)

        # 戦術メモ
        strategy_group = QGroupBox("戦術・立ち回りメモ")
        strategy_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin: 5px 0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        strategy_layout = QVBoxLayout(strategy_group)
        
        self.strategy_edit = QTextEdit()
        self.strategy_edit.setMaximumHeight(80)
        self.strategy_edit.setPlaceholderText("ローテーション、立ち回り、注意点など...")
        self.strategy_edit.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
        strategy_layout.addWidget(self.strategy_edit)
        
        layout.addWidget(strategy_group)

    def get_detail_data(self):
        """詳細データを取得"""
        characters = []
        for char_widget in self.character_widgets:
            characters.append({
                'name': char_widget['name'].text(),
                'level': char_widget['level'].value(),
                'eidolon': char_widget['eidolon'].value(),
                'lightcone': char_widget['lightcone'].text(),
                'superimpose': char_widget['superimpose'].value(),
                'main_stats': {part: combo.currentText() for part, combo in char_widget['main_stats'].items()},
                'relic_set': char_widget['relic_set'].toPlainText(),
                'sub_stats': char_widget['sub_stats'].toPlainText()
            })
        
        return {
            'characters': characters,
            'strategy': self.strategy_edit.toPlainText()
        }

    def set_detail_data(self, data):
        """詳細データを設定"""
        if not data:
            return
        
        characters = data.get('characters', [])
        for i, char_widget in enumerate(self.character_widgets):
            if i < len(characters):
                char_data = characters[i]
                char_widget['name'].setText(char_data.get('name', ''))
                char_widget['level'].setValue(char_data.get('level', 80))
                char_widget['eidolon'].setValue(char_data.get('eidolon', 0))
                char_widget['lightcone'].setText(char_data.get('lightcone', ''))
                char_widget['superimpose'].setValue(char_data.get('superimpose', 1))
                
                main_stats = char_data.get('main_stats', {})
                for part, combo in char_widget['main_stats'].items():
                    if part in main_stats:
                        index = combo.findText(main_stats[part])
                        if index >= 0:
                            combo.setCurrentIndex(index)
                
                char_widget['relic_set'].setPlainText(char_data.get('relic_set', ''))
                char_widget['sub_stats'].setPlainText(char_data.get('sub_stats', ''))
        
        self.strategy_edit.setPlainText(data.get('strategy', ''))

class TeamCompositionWidget(QWidget):
    """編成管理ウィジェット"""
    def __init__(self):
        super().__init__()
        self.team_rows = []
        self.detail_widgets = {}
        self.next_row_id = 1
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_data_now)
        self.setup_ui()

    def save_data_delayed(self):
        """データ保存を500ms遅延実行（リアルタイム保存用）"""
        self.save_timer.stop()
        self.save_timer.start(500)
    
    def save_data_now(self):
        """実際のデータ保存処理"""
        # 親ウィジェットから StarRailMemo インスタンスを取得
        parent = self.parent()
        while parent and not hasattr(parent, 'save_settings'):
            parent = parent.parent()
        if parent and hasattr(parent, 'save_settings'):
            parent.save_settings()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # ボタン行
        button_layout = QHBoxLayout()
        
        # 追加ボタン
        add_button = QPushButton("+ 編成を追加")
        add_button.setFixedHeight(40)
        add_button.setStyleSheet("""
            QPushButton {
                background: #f0f8ff;
                border: 2px dashed #4a90e2;
                border-radius: 5px;
                padding: 10px;
                color: #4a90e2;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e6f3ff;
            }
        """)
        add_button.clicked.connect(self.add_team_row)
        button_layout.addWidget(add_button)
        
        # コピーボタン
        copy_button = QPushButton("📋 編成をコピー")
        copy_button.setFixedHeight(40)
        copy_button.setStyleSheet("""
            QPushButton {
                background: #f0fff0;
                border: 2px solid #90ee90;
                border-radius: 5px;
                padding: 10px;
                color: #228b22;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e6ffe6;
            }
        """)
        copy_button.clicked.connect(self.copy_teams_to_clipboard)
        button_layout.addWidget(copy_button)
        
        layout.addLayout(button_layout)
        
        # ヘッダー
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_label = QLabel("キャラ編成")
        header_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #333;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        score_label = QLabel("スコア")
        score_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #333;")
        header_layout.addWidget(score_label)
        
        # 削除ボタン用のスペース
        header_layout.addWidget(QLabel("  "))
        
        layout.addLayout(header_layout)
        
        # スクロール可能な編成行一覧
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 5px;
                background: #fafafa;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)
        
        self.scroll_widget = QWidget()
        self.rows_layout = QVBoxLayout(self.scroll_widget)
        self.rows_layout.setContentsMargins(10, 10, 10, 10)
        self.rows_layout.setSpacing(10)
        # 重要: 上詰めにするため、最後にストレッチを追加
        self.rows_layout.addStretch()
        
        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)

    def copy_teams_to_clipboard(self):
        """編成情報をクリップボードにコピー"""
        if not self.team_rows:
            return
        
        copy_text = []
        for i, row in enumerate(self.team_rows):
            row_data = row.get_simple_data()
            characters = row_data.get('characters', [])
            score = row_data.get('score', '')
            
            # キャラクター情報を整理
            char_parts = []
            for char in characters:
                name = char.get('name', '').strip()
                if name:  # 名前が入力されている場合のみ追加
                    eidolon = char.get('eidolon', 0)
                    superimpose = char.get('superimpose', 1)
                    char_parts.append(f"{name} E{eidolon} S{superimpose}")
            
            if char_parts:  # キャラクターが1人以上いる場合
                team_text = " / ".join(char_parts)
                if score.strip():
                    team_text += f" - スコア: {score}"
                copy_text.append(team_text)
        
        if copy_text:
            # クリップボードにコピー
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(copy_text))
        else:
            QMessageBox.warning(self.parent(), "コピーエラー", 
                              "コピー可能な編成がありません。")

    def add_team_row(self):
        """編成行を追加"""
        row_id = self.next_row_id
        self.next_row_id += 1
        
        team_row = SimpleTeamRow(row_id, self)
        self.team_rows.append(team_row)
        
        # ストレッチの前に挿入（最後から2番目の位置）
        insert_index = self.rows_layout.count() - 1
        self.rows_layout.insertWidget(insert_index, team_row)

    def delete_team_row(self, row_id):
        """編成行を削除"""
        for i, row in enumerate(self.team_rows):
            if row.row_id == row_id:
                row.deleteLater()
                self.team_rows.pop(i)
                break

    def get_all_team_data(self):
        """全編成データを取得"""
        teams = []
        for row in self.team_rows:
            row_data = row.get_simple_data()
            row_data['row_id'] = row.row_id
            teams.append(row_data)
        return teams

    def set_all_team_data(self, teams_data):
        """全編成データを設定"""
        if not teams_data:
            return
        
        # 既存の行をクリア（ストレッチ以外）
        for row in self.team_rows:
            row.deleteLater()
        self.team_rows.clear()
        
        # データから行を復元
        for team_data in teams_data:
            row_id = team_data.get('row_id', self.next_row_id)
            self.next_row_id = max(self.next_row_id, row_id + 1)
            
            team_row = SimpleTeamRow(row_id, self)
            team_row.set_simple_data(team_data)
            self.team_rows.append(team_row)
            
            # ストレッチの前に挿入
            insert_index = self.rows_layout.count() - 1
            self.rows_layout.insertWidget(insert_index, team_row)

class StarRailMemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("スターレイル メモアプリ")
        # 最大化状態で起動
        self.showMaximized()
        
        # シンプルな白黒テーマを設定
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #333333;
                font-family: 'Meiryo', sans-serif;
            }
            QFrame {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #f8f8f8;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px 12px;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #d8d8d8;
            }
            QPushButton:checked {
                background-color: #333333;
                color: #ffffff;
                font-weight: bold;
            }
        """)

        self.sections = {}
        self.section_data = {}
        self.section_ui = {}
        self.section_selector_buttons = []
        self.name_to_button = {}
        self.last_section = None
        self._first_show = True  # 初回表示フラグ
        self._initialization_complete = False  # 初期化完了フラグ

        self.section_stack = QStackedWidget()
        self.main_layout = QVBoxLayout()

        # タブバー
        self.tab_bar_frame = QFrame()
        self.tab_bar_frame.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        self.tab_bar_layout = QHBoxLayout(self.tab_bar_frame)
        self.tab_bar_layout.setContentsMargins(5, 5, 5, 5)
        self.tab_bar_layout.setSpacing(2)

        self.main_layout.addWidget(self.tab_bar_frame)

        # 追加ボタン
        self.add_button = QPushButton("＋")
        self.add_button.setFixedSize(30, 25)
        self.add_button.clicked.connect(self.prompt_new_section_name)
        self.tab_bar_layout.addWidget(self.add_button)
        self.tab_bar_layout.addStretch()

        self.main_layout.addWidget(self.section_stack)
        self.setLayout(self.main_layout)

        # 設定を読み込み
        self.load_settings()
        
        # 保存されたセクションを復元（特別なキー以外）
        sections_to_restore = []
        for name in self.section_data:
            if name not in ["_last_section", "_window_geometry"]:
                sections_to_restore.append(name)
        
        # 保存されたセクションがある場合は復元、ない場合のみデフォルト作成
        if sections_to_restore:
            for name in sections_to_restore:
                self.add_section(name=name)
        else:
            # 初回起動時のみデフォルトセクションを作成
            default_name = "セクション 1"
            self.section_data[default_name] = {
                "content": None,
                "phase": None,
                "teams": []
            }
            self.add_section(name=default_name)
        
        # 最後に開いていたセクションを復元
        if self.last_section and self.last_section in self.sections:
            self.change_section_by_name(self.last_section)
        elif self.sections:
            # last_sectionが無効な場合は最初のセクションを選択
            first_section = list(self.sections.keys())[0]
            self.change_section_by_name(first_section)
        
        # 初期化完了
        self._initialization_complete = True

    def prompt_new_section_name(self):
        name, ok = QInputDialog.getText(self, "新規セクション", "セクション名を入力:")
        if ok and name:
            if name in self.sections:
                QMessageBox.warning(self, "エラー", "すでにある名前です")
            else:
                self.add_section(name=name)

    def add_section(self, name=None):
        if not name:
            name = f"セクション {len(self.sections) + 1}"
        if name in self.sections:
            return
        
        # デフォルトデータ（既存データがない場合のみ作成）
        if name not in self.section_data:
            self.section_data[name] = {
                "content": None, 
                "phase": None,
                "teams": []
            }

        # セクションウィジェット作成
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)

        # コンテンツ選択
        content_layout = QHBoxLayout()
        content_label = QLabel("コンテンツ選択:")
        content_label.setFont(QFont("Meiryo", 10, QFont.Bold))
        content_layout.addWidget(content_label)

        content_buttons = []
        for content in ["忘却の庭", "虚構叙事", "末日の幻影"]:
            btn = QPushButton(content)
            btn.setCheckable(True)
            btn.setFont(QFont("Meiryo", 9))
            btn.clicked.connect(lambda checked, b=btn, n=name: self.select_content(n, b))
            content_buttons.append(btn)
            content_layout.addWidget(btn)

        phase_label = QLabel(" | 区分:")
        phase_label.setFont(QFont("Meiryo", 10, QFont.Bold))
        content_layout.addWidget(phase_label)

        phase_buttons = []
        for phase in ["前半", "後半"]:
            btn = QPushButton(phase)
            btn.setCheckable(True)
            btn.setFont(QFont("Meiryo", 9))
            btn.clicked.connect(lambda checked, b=btn, n=name: self.select_phase(n, b))
            phase_buttons.append(btn)
            content_layout.addWidget(btn)

        content_layout.addStretch()
        section_layout.addLayout(content_layout)

        # 編成管理ウィジェット
        team_widget = TeamCompositionWidget()
        section_layout.addWidget(team_widget)

        self.section_stack.addWidget(section_widget)
        self.sections[name] = section_widget

        self.section_ui[name] = {
            "content_buttons": content_buttons,
            "phase_buttons": phase_buttons,
            "team_widget": team_widget
        }

        # タブ作成
        tab_frame = QFrame()
        tab_frame.setStyleSheet("""
            QFrame { 
                border: 1px solid #ccc; 
                border-bottom: none; 
                border-top-left-radius: 5px; 
                border-top-right-radius: 5px; 
                background-color: #f8f8f8; 
            }
        """)
        tab_layout = QHBoxLayout(tab_frame)
        tab_layout.setContentsMargins(5, 0, 5, 0)
        tab_layout.setSpacing(5)

        tab_button = QPushButton(name)
        tab_button.setCheckable(True)
        tab_button.setStyleSheet("""
            QPushButton { 
                border: none; 
                background: transparent; 
                padding: 8px 12px; 
                font-size: 11px;
                color: #666;
            }
            QPushButton:checked { 
                background-color: #ffffff; 
                font-weight: bold; 
                border-radius: 3px;
                color: #333;
            }
        """)
        tab_button.clicked.connect(lambda checked, n=name: self.change_section_by_name(n))
        tab_button.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_button.customContextMenuRequested.connect(lambda pos, n=name: self.rename_section(n))

        close_button = QToolButton()
        close_button.setText("×")
        close_button.setFixedSize(16, 16)
        close_button.setStyleSheet("""
            QToolButton { 
                color: #666; 
                background-color: transparent; 
                border: 1px solid #ddd; 
                font-weight: bold; 
                padding: 0; 
                border-radius: 8px; 
            } 
            QToolButton:hover { 
                color: #333; 
                background-color: #f0f0f0; 
            }
        """)
        close_button.clicked.connect(lambda _, n=name, f=tab_frame: self.remove_section_by_name(n, f))

        tab_layout.addWidget(tab_button)
        tab_layout.addWidget(close_button)
        tab_frame.setLayout(tab_layout)

        self.section_selector_buttons.append(tab_button)
        self.name_to_button[name] = tab_button
        self.tab_bar_layout.insertWidget(self.tab_bar_layout.count() - 2, tab_frame)

        self.highlight_selected_section(name)
        self.section_stack.setCurrentWidget(section_widget)
        
        # セクション作成直後にデータを復元
        if not self._initialization_complete:
            # 起動時の復元の場合は保存データから復元
            QTimer.singleShot(100, lambda: self.restore_section_state(name))
        else:
            # 新規セクション作成時はデフォルトで1行追加（編成が空の場合のみ）
            QTimer.singleShot(100, lambda: self.ensure_minimum_teams(name))

    def rename_section(self, name):
        new_name, ok = QInputDialog.getText(self, "セクション名変更", "新しい名前:", text=name)
        if ok and new_name and new_name != name:
            if new_name in self.sections:
                QMessageBox.warning(self, "エラー", "すでにある名前です")
                return
            self.section_data[new_name] = self.section_data.pop(name)
            self.sections[new_name] = self.sections.pop(name)
            self.section_ui[new_name] = self.section_ui.pop(name)
            btn = self.name_to_button.pop(name)
            btn.setText(new_name)
            self.name_to_button[new_name] = btn
            btn.clicked.disconnect()
            btn.clicked.connect(lambda checked, n=new_name: self.change_section_by_name(n))
            btn.customContextMenuRequested.connect(lambda pos, n=new_name: self.rename_section(n))
            self.highlight_selected_section(new_name)
            self.save_settings()

    def remove_section_by_name(self, name, frame):
        if name in self.sections:
            widget = self.sections.pop(name)
            self.section_stack.removeWidget(widget)
            if name in self.section_data:
                del self.section_data[name]
            if name in self.section_ui:
                del self.section_ui[name]
            if name in self.name_to_button:
                del self.name_to_button[name]
                # セクションボタンリストからも削除
                for btn in self.section_selector_buttons:
                    if btn.text() == name:
                        self.section_selector_buttons.remove(btn)
                        break
            frame.deleteLater()
            self.save_settings()

    def change_section_by_name(self, section_name):
        if section_name in self.sections:
            # 現在のセクションのデータを保存
            self.save_all_team_data()
            # セクションを切り替え
            self.section_stack.setCurrentWidget(self.sections[section_name])
            self.highlight_selected_section(section_name)
            # データ復元は少し遅延させる
            QTimer.singleShot(50, lambda: self.restore_section_state(section_name))

    def highlight_selected_section(self, active_name):
        for name, btn in self.name_to_button.items():
            btn.setChecked(name == active_name)

    def select_content(self, section_name, button):
        # 現在のデータを保存
        self.save_all_team_data()
        buttons = self.section_ui.get(section_name, {}).get("content_buttons", [])
        for b in buttons:
            b.setChecked(False)
        button.setChecked(True)
        self.section_data[section_name]["content"] = button.text()
        if self._initialization_complete:
            self.save_settings()

    def select_phase(self, section_name, button):
        # 現在のデータを保存
        self.save_all_team_data()
        buttons = self.section_ui.get(section_name, {}).get("phase_buttons", [])
        for b in buttons:
            b.setChecked(False)
        button.setChecked(True)
        self.section_data[section_name]["phase"] = button.text()
        if self._initialization_complete:
            self.save_settings()

    def closeEvent(self, event):
        """アプリケーション終了時に全てのデータを保存"""
        print("アプリケーションを終了中... データを保存しています")
        self.save_all_team_data()
        self.save_settings()
        print("データ保存完了")
        event.accept()

    def save_all_team_data(self):
        """全セクションの編成データを保存"""
        for name, ui in self.section_ui.items():
            if "team_widget" in ui:
                self.section_data[name]["teams"] = ui["team_widget"].get_all_team_data()

    def save_settings(self):
        if not self._initialization_complete:
            return  # 初期化中は保存しない
            
        self.save_all_team_data()
        try:
            data_to_save = self.section_data.copy()
            # 現在表示されているセクションを記録
            current_widget = self.section_stack.currentWidget()
            for name, widget in self.sections.items():
                if widget == current_widget:
                    data_to_save["_last_section"] = name
                    break
            
            # テキストファイルとして保存
            with open("settings.txt", "w", encoding="utf-8") as f:
                f.write("=== STARRAI MEMO SETTINGS ===\n")
                f.write(f"LAST_SECTION: {data_to_save.get('_last_section', 'None')}\n")
                f.write(f"SECTIONS_COUNT: {len([k for k in data_to_save.keys() if not k.startswith('_')])}\n")
                f.write("\n")
                
                # 各セクションのデータを保存
                for section_name, section_data in data_to_save.items():
                    if section_name.startswith('_'):
                        continue  # 特別なキーはスキップ
                    
                    f.write(f"[SECTION: {section_name}]\n")
                    f.write(f"CONTENT: {section_data.get('content', 'None')}\n")
                    f.write(f"PHASE: {section_data.get('phase', 'None')}\n")
                    
                    teams = section_data.get('teams', [])
                    f.write(f"TEAMS_COUNT: {len(teams)}\n")
                    
                    for i, team in enumerate(teams):
                        f.write(f"  [TEAM_{i+1}]\n")
                        f.write(f"  ROW_ID: {team.get('row_id', 0)}\n")
                        f.write(f"  SCORE: {team.get('score', '')}\n")
                        
                        characters = team.get('characters', [])
                        for j, char in enumerate(characters):
                            f.write(f"    [CHAR_{j+1}]\n")
                            f.write(f"    NAME: {char.get('name', '')}\n")
                            f.write(f"    EIDOLON: {char.get('eidolon', 0)}\n")
                            f.write(f"    SUPERIMPOSE: {char.get('superimpose', 1)}\n")
                            f.write(f"    LEVEL: {char.get('level', 80)}\n")
                            f.write(f"    LIGHTCONE: {char.get('lightcone', '')}\n")
                            f.write(f"    MEMO: {char.get('memo', '').replace(chr(10), '\\n')}\n")
                            f.write(f"    DETAIL_SHOWN: {char.get('detail_shown', False)}\n")
                            
                            # メイン効果
                            main_stats = char.get('main_stats', {})
                            f.write(f"    MAIN_STATS: {main_stats.get('胴', 'HP%')}|{main_stats.get('脚', 'HP%')}|{main_stats.get('縄', 'HP%')}|{main_stats.get('球', 'HP%')}\n")
                    
                    f.write("\n")
                
            print(f"設定をテキストファイルに保存しました: {len([k for k in data_to_save.keys() if not k.startswith('_')])}セクション")
                
        except Exception as e:
            print(f"設定保存エラー: {e}")

    def load_settings(self):
        self.last_section = None
        
        # まずテキストファイルを確認
        if os.path.exists("settings.txt"):
            try:
                self.section_data = {}
                current_section = None
                current_team = None
                current_char = None
                
                with open("settings.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("==="):
                        continue
                    
                    if line.startswith("LAST_SECTION:"):
                        self.last_section = line.split(":", 1)[1].strip()
                        if self.last_section == "None":
                            self.last_section = None
                    
                    elif line.startswith("[SECTION:"):
                        section_name = line[9:-1]  # [SECTION: と ] を除去
                        current_section = section_name
                        self.section_data[current_section] = {
                            "content": None,
                            "phase": None,
                            "teams": []
                        }
                    
                    elif line.startswith("CONTENT:") and current_section:
                        content = line.split(":", 1)[1].strip()
                        self.section_data[current_section]["content"] = content if content != "None" else None
                    
                    elif line.startswith("PHASE:") and current_section:
                        phase = line.split(":", 1)[1].strip()
                        self.section_data[current_section]["phase"] = phase if phase != "None" else None
                    
                    elif line.startswith("  [TEAM_"):
                        current_team = {
                            "row_id": 1,
                            "score": "",
                            "characters": []
                        }
                        self.section_data[current_section]["teams"].append(current_team)
                    
                    elif line.startswith("  ROW_ID:") and current_team is not None:
                        current_team["row_id"] = int(line.split(":", 1)[1].strip())
                    
                    elif line.startswith("  SCORE:") and current_team is not None:
                        current_team["score"] = line.split(":", 1)[1].strip()
                    
                    elif line.startswith("    [CHAR_"):
                        current_char = {
                            "name": "",
                            "eidolon": 0,
                            "superimpose": 1,
                            "level": 80,
                            "lightcone": "",
                            "memo": "",
                            "detail_shown": False,
                            "main_stats": {"胴": "HP%", "脚": "HP%", "縄": "HP%", "球": "HP%"}
                        }
                        current_team["characters"].append(current_char)
                    
                    elif line.startswith("    NAME:") and current_char is not None:
                        current_char["name"] = line.split(":", 1)[1].strip()
                    
                    elif line.startswith("    EIDOLON:") and current_char is not None:
                        current_char["eidolon"] = int(line.split(":", 1)[1].strip())
                    
                    elif line.startswith("    SUPERIMPOSE:") and current_char is not None:
                        current_char["superimpose"] = int(line.split(":", 1)[1].strip())
                    
                    elif line.startswith("    LEVEL:") and current_char is not None:
                        current_char["level"] = int(line.split(":", 1)[1].strip())
                    
                    elif line.startswith("    LIGHTCONE:") and current_char is not None:
                        current_char["lightcone"] = line.split(":", 1)[1].strip()
                    
                    elif line.startswith("    MEMO:") and current_char is not None:
                        memo = line.split(":", 1)[1].strip()
                        current_char["memo"] = memo.replace("\\n", "\n")
                    
                    elif line.startswith("    DETAIL_SHOWN:") and current_char is not None:
                        current_char["detail_shown"] = line.split(":", 1)[1].strip().lower() == "true"
                    
                    elif line.startswith("    MAIN_STATS:") and current_char is not None:
                        stats_str = line.split(":", 1)[1].strip()
                        stats_parts = stats_str.split("|")
                        if len(stats_parts) >= 4:
                            current_char["main_stats"] = {
                                "胴": stats_parts[0],
                                "脚": stats_parts[1],
                                "縄": stats_parts[2],
                                "球": stats_parts[3]
                            }
                
                print(f"テキスト設定を読み込みました: {len(self.section_data)}セクション")
                print(f"セクション一覧: {list(self.section_data.keys())}")
                    
            except Exception as e:
                print(f"テキスト設定読み込みエラー: {e}")
                # テキストが失敗した場合、pickleからの移行を試行
                self.migrate_from_pickle()
        else:
            # テキストファイルがない場合、pickleからの移行を試行
            self.migrate_from_pickle()

    def migrate_from_pickle(self):
        """pickleファイルからテキストへの移行"""
        if os.path.exists("settings.pkl"):
            try:
                import pickle
                with open("settings.pkl", "rb") as f:
                    data = pickle.load(f)
                    if isinstance(data, dict):
                        self.last_section = data.pop("_last_section", None)
                        data.pop("_window_geometry", None)
                        self.section_data = data
                        print(f"pickle設定からデータを移行しました: {len(self.section_data)}セクション")
                        # 移行後、テキストで保存し直す
                        self.save_settings()
                        # 古いpickleファイルをリネーム（バックアップとして）
                        if os.path.exists("settings.pkl"):
                            os.rename("settings.pkl", "settings_backup.pkl")
                            print("旧pickleファイルをsettings_backup.pklにリネームしました")
                    else:
                        self.section_data = {}
                        print("pickle設定ファイルが無効な形式です")
            except Exception as e:
                print(f"pickle設定移行エラー: {e}")
                # pickleも失敗した場合、JSONからの移行を試行
                self.migrate_from_json()
        else:
            # pickleファイルがない場合、JSONからの移行を試行
            self.migrate_from_json()

    def migrate_from_json(self):
        """JSONファイルからテキストへの移行"""
        if os.path.exists("settings.json"):
            try:
                import json
                with open("settings.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.last_section = data.pop("_last_section", None)
                        data.pop("_window_geometry", None)
                        self.section_data = data
                        print(f"JSON設定からデータを移行しました: {len(self.section_data)}セクション")
                        # 移行後、テキストで保存し直す
                        self.save_settings()
                        # 古いJSONファイルをリネーム（バックアップとして）
                        if os.path.exists("settings.json"):
                            os.rename("settings.json", "settings_backup.json")
                            print("旧JSONファイルをsettings_backup.jsonにリネームしました")
                    else:
                        self.section_data = {}
                        print("JSON設定ファイルが無効な形式です")
            except Exception as e:
                print(f"JSON設定移行エラー: {e}")
                self.section_data = {}
        else:
            self.section_data = {}
            print("設定ファイルが見つかりません")

    def ensure_minimum_teams(self, section_name):
        """新規セクションで編成が空の場合、最低1行は追加する"""
        if section_name in self.section_ui:
            ui = self.section_ui[section_name]
            if "team_widget" in ui:
                team_widget = ui["team_widget"]
                if not team_widget.team_rows:  # 編成行が空の場合
                    team_widget.add_team_row()
                    print(f"新規セクション '{section_name}' にデフォルト編成行を追加しました")

    def restore_section_state(self, section_name):
        """セクションの状態を復元"""
        if section_name not in self.section_data:
            print(f"セクション '{section_name}' のデータが見つかりません")
            return
            
        data = self.section_data[section_name]
        ui = self.section_ui.get(section_name, {})
        
        print(f"セクション '{section_name}' の状態を復元中...")
        print(f"コンテンツ: {data.get('content')}, フェーズ: {data.get('phase')}, チーム数: {len(data.get('teams', []))}")
        
        # コンテンツ・フェーズボタンの復元
        for btn in ui.get("content_buttons", []):
            btn.setChecked(btn.text() == data.get("content"))
        for btn in ui.get("phase_buttons", []):
            btn.setChecked(btn.text() == data.get("phase"))
        
        # 編成データの復元
        if "team_widget" in ui and "teams" in data:
            teams_data = data["teams"]
            if teams_data:  # データが存在する場合のみ復元
                ui["team_widget"].set_all_team_data(teams_data)
                print(f"編成データを復元しました: {len(teams_data)}編成")
            else:
                print("編成データが空です")
    
    def resizeEvent(self, event):
        """ウィンドウサイズ変更時の処理（即座に保存はしない）"""
        super().resizeEvent(event)
    
    def moveEvent(self, event):
        """ウィンドウ移動時の処理（即座に保存はしない）"""
        super().moveEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StarRailMemo()
    window.show()
    sys.exit(app.exec_())