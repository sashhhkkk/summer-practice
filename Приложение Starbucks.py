import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StarbucksAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ данных Starbucks")
        self.root.geometry("1000x700")

        self.df = None
        self.filtered_df = None

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #верхняя панель с кнопками
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=5)

        self.load_button = ttk.Button(self.top_frame, text="Загрузить CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.info_button = ttk.Button(self.top_frame, text="Информация о данных", command=self.show_data_info)
        self.info_button.pack(side=tk.LEFT, padx=5)

        self.recommend_button = ttk.Button(self.top_frame, text="Рекомендации", command=self.show_recommendations)
        self.recommend_button.pack(side=tk.LEFT, padx=5)

        #панель фильтров
        self.filter_frame = ttk.LabelFrame(self.main_frame, text="Фильтры")
        self.filter_frame.pack(fill=tk.X, pady=5)

        #категория напитка
        ttk.Label(self.filter_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.filter_frame, textvariable=self.category_var, state="readonly")
        self.category_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        #калории
        ttk.Label(self.filter_frame, text="Калории до:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.calories_var = tk.StringVar()
        self.calories_entry = ttk.Entry(self.filter_frame, textvariable=self.calories_var)
        self.calories_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        #кофеин
        ttk.Label(self.filter_frame, text="Кофеин от:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.caffeine_min_var = tk.StringVar()
        self.caffeine_min_entry = ttk.Entry(self.filter_frame, textvariable=self.caffeine_min_var)
        self.caffeine_min_entry.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)

        #сахар
        ttk.Label(self.filter_frame, text="Сахар до:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.sugar_var = tk.StringVar()
        self.sugar_entry = ttk.Entry(self.filter_frame, textvariable=self.sugar_var)
        self.sugar_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        #белок
        ttk.Label(self.filter_frame, text="Белок от:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.protein_var = tk.StringVar()
        self.protein_entry = ttk.Entry(self.filter_frame, textvariable=self.protein_var)
        self.protein_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        #кнопка применения фильтров
        self.apply_button = ttk.Button(self.filter_frame, text="Применить фильтры", command=self.apply_filters)
        self.apply_button.grid(row=1, column=4, columnspan=2, padx=5, pady=5)

        #панель для отображения данных и графиков
        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        #таблица с данными
        self.tree_frame = ttk.Frame(self.display_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        #панель для графиков
        self.graph_frame = ttk.Frame(self.display_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Статус
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def load_csv(self):
        try:
            self.df = pd.read_csv('starbucks_processed.csv')

            self.df['beverage_category'] = self.df['beverage_category'].astype(str)

            categories = sorted(self.df['beverage_category'].unique())
            self.category_combobox['values'] = categories

            self.status_var.set(f"Данные загружены. Записей: {len(self.df)}")
            self.show_data_in_table(self.df)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def show_data_info(self):
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return

        info_window = tk.Toplevel(self.root)
        info_window.title("Информация о данных")
        info_window.geometry("600x400")

        info_text = tk.Text(info_window, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #основная информация
        info = []
        info.append(f"Всего записей: {len(self.df)}")
        info.append(f"Колонки: {', '.join(self.df.columns)}")
        info.append("\nОписательная статистика для числовых колонок:")

        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            info.append(f"\n{col}:")
            info.append(f"  Среднее: {self.df[col].mean():.2f}")
            info.append(f"  Медиана: {self.df[col].median():.2f}")
            info.append(f"  Минимум: {self.df[col].min()}")
            info.append(f"  Максимум: {self.df[col].max()}")
            info.append(f"  Стандартное отклонение: {self.df[col].std():.2f}")

        info_text.insert(tk.END, "\n".join(info))
        info_text.config(state=tk.DISABLED)

    def apply_filters(self):
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return

        self.filtered_df = self.df.copy()

        #применяем фильтры
        try:
            #категория
            category = self.category_var.get()
            if category:
                self.filtered_df = self.filtered_df[self.filtered_df['beverage_category'] == category]

            #калории
            calories = self.calories_var.get()
            if calories:
                self.filtered_df = self.filtered_df[self.filtered_df['calories'] <= float(calories)]

            #кофеин
            caffeine_min = self.caffeine_min_var.get()
            if caffeine_min:
                self.filtered_df = self.filtered_df[self.filtered_df['caffeine_mg'] >= float(caffeine_min)]

            #сахар
            sugar = self.sugar_var.get()
            if sugar:
                self.filtered_df = self.filtered_df[self.filtered_df['sugars_g'] <= float(sugar)]

            #белок
            protein = self.protein_var.get()
            if protein:
                self.filtered_df = self.filtered_df[self.filtered_df['protein_g'] >= float(protein)]

            self.status_var.set(f"Найдено записей: {len(self.filtered_df)}")
            self.show_data_in_table(self.filtered_df)
            self.show_graphs(self.filtered_df)

        except ValueError as e:
            messagebox.showerror("Ошибка", "Проверьте правильность введенных значений фильтров")

    def show_data_in_table(self, df):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)

        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def show_graphs(self, df):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if len(df) == 0:
            return

        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle("Анализ напитков Starbucks", fontsize=14)

        #распределение калорий
        axes[0, 0].hist(df['calories'], bins=20, color='#006241', edgecolor='black')
        axes[0, 0].set_title('Распределение калорийности')
        axes[0, 0].set_xlabel('Калории')
        axes[0, 0].set_ylabel('Количество напитков')
        axes[0, 0].grid(axis='y', alpha=0.5)

        #содержание сахара по категориям
        if 'beverage_category' in df.columns:
            sugar_by_category = df.groupby('beverage_category')['sugars_g'].mean().sort_values(ascending=False)
            sugar_by_category.plot(kind='bar', ax=axes[0, 1], color='#1E3932')
            axes[0, 1].set_title('Среднее содержание сахара по категориям')
            axes[0, 1].set_xlabel('Категория напитка')
            axes[0, 1].set_ylabel('Среднее содержание сахара (г)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            axes[0, 1].grid(axis='y', alpha=0.5)

        #корреляция калорий и сахара
        axes[1, 0].scatter(df['sugars_g'], df['calories'], color='#d4e8e1', alpha=0.6)
        axes[1, 0].set_title('Корреляция сахара и калорий')
        axes[1, 0].set_xlabel('Сахар (г)')
        axes[1, 0].set_ylabel('Калории')
        axes[1, 0].grid(alpha=0.3)

        #содержание кофеина
        if 'caffeine_mg' in df.columns:
            axes[1, 1].boxplot(df['caffeine_mg'].dropna(), patch_artist=True,
                               boxprops=dict(facecolor='#006241'))
            axes[1, 1].set_title('Распределение кофеина')
            axes[1, 1].set_ylabel('Кофеин (мг)')
            axes[1, 1].grid(axis='y', alpha=0.3)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_recommendations(self):
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return

        rec_window = tk.Toplevel(self.root)
        rec_window.title("Рекомендации для Starbucks")
        rec_window.geometry("800x600")

        notebook = ttk.Notebook(rec_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #вкладка с общими рекомендациями
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Общие рекомендации")

        general_text = tk.Text(general_frame, wrap=tk.WORD)
        general_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        recommendations = [
            "1. Оптимизация рецептур:",
            "   - Снизить содержание сахара в напитках Frappuccino и сладких латте",
            "   - Разработать 'легкие' версии популярных напитков с пониженной калорийностью",
            "",
            "2. Сегментация меню:",
            "   - Создать отдельные категории для здоровых напитков (низкокалорийные, высокобелковые, без сахара)",
            "   - Продвигать напитки с высоким содержанием белка среди спортсменов и ЗОЖ-аудитории",
            "",
            "3. Маркировка:",
            "   - Добавить информацию о пищевой ценности на меню или в приложение",
            "   - Разработать систему фильтрации напитков по диетическим требованиям",
            "",
            "4. Разработка новых продуктов:",
            "   - Создать 'здоровые' наборы напитков для разных целевых групп",
            "   - Предложить больше вариантов с альтернативными видами молока (соевое, миндальное, овсяное)"
        ]

        general_text.insert(tk.END, "\n".join(recommendations))
        general_text.config(state=tk.DISABLED)

        #вкладка с рекомендациями по категориям
        category_frame = ttk.Frame(notebook)
        notebook.add(category_frame, text="По категориям")

        category_text = tk.Text(category_frame, wrap=tk.WORD)
        category_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if 'beverage_category' in self.df.columns:
            category_rec = []
            for category in sorted(self.df['beverage_category'].unique()):
                cat_df = self.df[self.df['beverage_category'] == category]
                avg_cal = cat_df['calories'].mean()
                avg_sugar = cat_df['sugars_g'].mean()

                category_rec.append(f"\n{category}:")
                category_rec.append(f"  - Средняя калорийность: {avg_cal:.1f} ккал")
                category_rec.append(f"  - Среднее содержание сахара: {avg_sugar:.1f} г")

                if avg_sugar > 30:
                    category_rec.append("  * Рекомендация: разработать варианты с пониженным содержанием сахара")
                if avg_cal > 250:
                    category_rec.append("  * Рекомендация: предложить 'легкие' версии с меньшей калорийностью")

            category_text.insert(tk.END, "\n".join(category_rec))
        else:
            category_text.insert(tk.END, "Данные о категориях не найдены")

        category_text.config(state=tk.DISABLED)


#запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = StarbucksAnalyticsApp(root)
    root.mainloop()