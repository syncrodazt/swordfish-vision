# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')

# スケール設定
ax1.set_xlim(0, 800)
ax1.set_ylim(0, 400)

# 軸のラベルを設定する。
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# データプロット
ax1.scatter(x_list, y_list, label='Tracking result')
plt.legend()
fig.tight_layout()

# グラフを表示する。
plt.show()
plt.close()
