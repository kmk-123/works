from flask import Flask, render_template_string, request, jsonify
import sqlite3
import json
from datetime import datetime
import math

app = Flask(__name__)

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('lol_stats.db')
    c = conn.cursor()
    
    # 플레이어 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS players
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL,
                  mmr INTEGER DEFAULT 1000,
                  games_played INTEGER DEFAULT 0,
                  wins INTEGER DEFAULT 0,
                  kills INTEGER DEFAULT 0,
                  deaths INTEGER DEFAULT 0,
                  assists INTEGER DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 경기 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS matches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  blue_team TEXT NOT NULL,
                  red_team TEXT NOT NULL,
                  blue_mmr_avg REAL,
                  red_mmr_avg REAL,
                  winning_team TEXT NOT NULL,
                  match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 경기 상세 스탯 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS match_stats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  match_id INTEGER,
                  player_id INTEGER,
                  team TEXT NOT NULL,
                  champion TEXT NOT NULL,
                  kills INTEGER DEFAULT 0,
                  deaths INTEGER DEFAULT 0,
                  assists INTEGER DEFAULT 0,
                  damage INTEGER DEFAULT 0,
                  gold INTEGER DEFAULT 0,
                  mmr_change INTEGER DEFAULT 0,
                  FOREIGN KEY (match_id) REFERENCES matches (id),
                  FOREIGN KEY (player_id) REFERENCES players (id))''')
    
    conn.commit()
    conn.close()

# MMR 계산 함수
def calculate_mmr_change(player_stats, team_won, team_avg_mmr, enemy_avg_mmr, team_stats):
    base_mmr = 20
    
    # 1. 팀 MMR 차이에 따른 배율 계산
    mmr_diff = team_avg_mmr - enemy_avg_mmr
    
    if team_won:
        # 이긴 경우: 상대가 강하면 더 많이 얻음
        if mmr_diff < 0:  # 약팀이 이김
            multiplier = 1 + abs(mmr_diff) / 200
        else:  # 강팀이 이김
            multiplier = max(0.5, 1 - mmr_diff / 200)
    else:
        # 진 경우: 상대가 약하면 더 많이 잃음
        if mmr_diff > 0:  # 강팀이 짐
            multiplier = 1 + mmr_diff / 200
        else:  # 약팀이 짐
            multiplier = max(0.5, 1 - abs(mmr_diff) / 200)
    
    team_mmr = base_mmr * multiplier
    
    # 2. 개인 성적 계산
    kda = (player_stats['kills'] + player_stats['assists']) / max(1, player_stats['deaths'])
    
    # 팀 내 평균 대비 개인 성적
    team_avg_damage = sum(p['damage'] for p in team_stats) / len(team_stats)
    team_avg_gold = sum(p['gold'] for p in team_stats) / len(team_stats)
    team_avg_kda = sum((p['kills'] + p['assists']) / max(1, p['deaths']) for p in team_stats) / len(team_stats)
    
    # 개인 성적 점수 (팀 평균 대비)
    damage_score = (player_stats['damage'] / max(1, team_avg_damage) - 1) * 5
    gold_score = (player_stats['gold'] / max(1, team_avg_gold) - 1) * 3
    kda_score = (kda / max(1, team_avg_kda) - 1) * 7
    
    personal_mmr = damage_score + gold_score + kda_score
    personal_mmr = max(-10, min(10, personal_mmr))  # -10 ~ +10 범위로 제한
    
    # 3. 최종 MMR 변화
    if team_won:
        total_change = team_mmr + personal_mmr
    else:
        total_change = -(team_mmr - personal_mmr)
    
    return round(total_change)

# HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LOL 전적 관리 시스템</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab {
            padding: 12px 24px;
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .tab:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .tab.active {
            background: white;
            color: #667eea;
            font-weight: bold;
        }
        
        .content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            display: none;
        }
        
        .content.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #5568d3;
        }
        
        .team-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }
        
        .team {
            padding: 20px;
            border-radius: 8px;
        }
        
        .blue-team {
            background: #e3f2fd;
            border: 2px solid #2196f3;
        }
        
        .red-team {
            background: #ffebee;
            border: 2px solid #f44336;
        }
        
        .player-input {
            margin-bottom: 15px;
            padding: 15px;
            background: white;
            border-radius: 6px;
        }
        
        .player-input h4 {
            margin-bottom: 10px;
            color: #333;
        }
        
        .stat-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        
        .stat-input {
            display: flex;
            flex-direction: column;
        }
        
        .stat-input label {
            font-size: 12px;
            margin-bottom: 4px;
        }
        
        .stat-input input {
            padding: 6px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        th {
            background: #f5f5f5;
            font-weight: 600;
            color: #333;
        }
        
        tr:hover {
            background: #f9f9f9;
        }
        
        .rank-1 { background: #ffd700 !important; }
        .rank-2 { background: #c0c0c0 !important; }
        .rank-3 { background: #cd7f32 !important; }
        
        .player-card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .player-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-box {
            background: white;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }
        
        .match-history {
            margin-top: 20px;
        }
        
        .match-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        
        .win { border-left-color: #4caf50; }
        .loss { border-left-color: #f44336; }
        
        .success-msg {
            background: #4caf50;
            color: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            display: none;
        }
        
        .error-msg {
            background: #f44336;
            color: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 LOL 전적 관리 시스템</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('ranking')">랭킹</button>
            <button class="tab" onclick="showTab('add-player')">플레이어 추가</button>
            <button class="tab" onclick="showTab('add-match')">경기 입력</button>
            <button class="tab" onclick="showTab('player-detail')">플레이어 상세</button>
        </div>
        
        <!-- 랭킹 탭 -->
        <div id="ranking" class="content active">
            <h2>🏆 MMR 랭킹</h2>
            <table id="ranking-table">
                <thead>
                    <tr>
                        <th>순위</th>
                        <th>플레이어</th>
                        <th>MMR</th>
                        <th>경기 수</th>
                        <th>승률</th>
                        <th>평균 KDA</th>
                    </tr>
                </thead>
                <tbody id="ranking-body">
                </tbody>
            </table>
        </div>
        
        <!-- 플레이어 추가 탭 -->
        <div id="add-player" class="content">
            <h2>➕ 플레이어 추가</h2>
            <div class="success-msg" id="player-success"></div>
            <div class="error-msg" id="player-error"></div>
            <div class="form-group">
                <label>플레이어 이름</label>
                <input type="text" id="player-name" placeholder="소환사명을 입력하세요">
            </div>
            <button onclick="addPlayer()">플레이어 추가</button>
        </div>
        
        <!-- 경기 입력 탭 -->
        <div id="add-match" class="content">
            <h2>⚔️ 경기 결과 입력</h2>
            <div class="success-msg" id="match-success"></div>
            <div class="error-msg" id="match-error"></div>
            
            <div class="form-group">
                <label>승리 팀</label>
                <select id="winning-team">
                    <option value="blue">블루팀</option>
                    <option value="red">레드팀</option>
                </select>
            </div>
            
            <div class="team-section">
                <div class="team blue-team">
                    <h3>🔵 블루팀</h3>
                    <div id="blue-team-players"></div>
                </div>
                
                <div class="team red-team">
                    <h3>🔴 레드팀</h3>
                    <div id="red-team-players"></div>
                </div>
            </div>
            
            <button onclick="submitMatch()" style="margin-top: 20px; width: 100%;">경기 결과 제출</button>
        </div>
        
        <!-- 플레이어 상세 탭 -->
        <div id="player-detail" class="content">
            <h2>📊 플레이어 상세 정보</h2>
            <div class="form-group">
                <label>플레이어 선택</label>
                <select id="detail-player-select" onchange="loadPlayerDetail()">
                    <option value="">플레이어를 선택하세요</option>
                </select>
            </div>
            <div id="player-detail-content"></div>
        </div>
    </div>
    
    <script>
        let players = [];
        
        function showTab(tabName) {
            document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'ranking') loadRanking();
            if (tabName === 'add-match') loadMatchForm();
            if (tabName === 'player-detail') loadPlayerSelect();
        }
        
        async function loadRanking() {
            const response = await fetch('/api/players');
            players = await response.json();
            
            const tbody = document.getElementById('ranking-body');
            tbody.innerHTML = '';
            
            players.forEach((player, idx) => {
                const winRate = player.games_played > 0 ? (player.wins / player.games_played * 100).toFixed(1) : 0;
                const kda = player.deaths > 0 ? ((player.kills + player.assists) / player.deaths).toFixed(2) : player.kills + player.assists;
                
                const row = document.createElement('tr');
                if (idx < 3) row.classList.add(`rank-${idx + 1}`);
                
                row.innerHTML = `
                    <td>${idx + 1}</td>
                    <td><strong>${player.name}</strong></td>
                    <td><strong>${player.mmr}</strong></td>
                    <td>${player.games_played}</td>
                    <td>${winRate}%</td>
                    <td>${kda}</td>
                `;
                tbody.appendChild(row);
            });
        }
        
        async function addPlayer() {
            const name = document.getElementById('player-name').value.trim();
            
            if (!name) {
                showMessage('player-error', '플레이어 이름을 입력하세요');
                return;
            }
            
            const response = await fetch('/api/players', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name})
            });
            
            const result = await response.json();
            
            if (result.success) {
                showMessage('player-success', `${name} 플레이어가 추가되었습니다!`);
                document.getElementById('player-name').value = '';
            } else {
                showMessage('player-error', result.message);
            }
        }
        
        async function loadMatchForm() {
            const response = await fetch('/api/players');
            players = await response.json();
            
            if (players.length < 10) {
                document.getElementById('match-error').style.display = 'block';
                document.getElementById('match-error').textContent = '경기를 입력하려면 최소 10명의 플레이어가 필요합니다';
                return;
            }
            
            const blueDiv = document.getElementById('blue-team-players');
            const redDiv = document.getElementById('red-team-players');
            
            blueDiv.innerHTML = '';
            redDiv.innerHTML = '';
            
            for (let i = 0; i < 5; i++) {
                blueDiv.innerHTML += createPlayerInput('blue', i);
                redDiv.innerHTML += createPlayerInput('red', i);
            }
        }
        
        function createPlayerInput(team, idx) {
            const options = players.map(p => `<option value="${p.id}">${p.name} (${p.mmr})</option>`).join('');
            
            return `
                <div class="player-input">
                    <h4>플레이어 ${idx + 1}</h4>
                    <select id="${team}-player-${idx}" class="player-select">
                        <option value="">선택</option>
                        ${options}
                    </select>
                    <input type="text" id="${team}-champion-${idx}" placeholder="챔피언" style="margin-top: 10px;">
                    <div class="stat-row">
                        <div class="stat-input">
                            <label>킬</label>
                            <input type="number" id="${team}-kills-${idx}" value="0" min="0">
                        </div>
                        <div class="stat-input">
                            <label>데스</label>
                            <input type="number" id="${team}-deaths-${idx}" value="0" min="0">
                        </div>
                        <div class="stat-input">
                            <label>어시</label>
                            <input type="number" id="${team}-assists-${idx}" value="0" min="0">
                        </div>
                    </div>
                    <div class="stat-row">
                        <div class="stat-input">
                            <label>딜량</label>
                            <input type="number" id="${team}-damage-${idx}" value="0" min="0">
                        </div>
                        <div class="stat-input">
                            <label>골드</label>
                            <input type="number" id="${team}-gold-${idx}" value="0" min="0">
                        </div>
                    </div>
                </div>
            `;
        }
        
        async function submitMatch() {
            const winningTeam = document.getElementById('winning-team').value;
            
            const matchData = {
                winning_team: winningTeam,
                blue_team: [],
                red_team: []
            };
            
            for (let i = 0; i < 5; i++) {
                const bluePlayer = {
                    player_id: document.getElementById(`blue-player-${i}`).value,
                    champion: document.getElementById(`blue-champion-${i}`).value,
                    kills: parseInt(document.getElementById(`blue-kills-${i}`).value) || 0,
                    deaths: parseInt(document.getElementById(`blue-deaths-${i}`).value) || 0,
                    assists: parseInt(document.getElementById(`blue-assists-${i}`).value) || 0,
                    damage: parseInt(document.getElementById(`blue-damage-${i}`).value) || 0,
                    gold: parseInt(document.getElementById(`blue-gold-${i}`).value) || 0
                };
                
                const redPlayer = {
                    player_id: document.getElementById(`red-player-${i}`).value,
                    champion: document.getElementById(`red-champion-${i}`).value,
                    kills: parseInt(document.getElementById(`red-kills-${i}`).value) || 0,
                    deaths: parseInt(document.getElementById(`red-deaths-${i}`).value) || 0,
                    assists: parseInt(document.getElementById(`red-assists-${i}`).value) || 0,
                    damage: parseInt(document.getElementById(`red-damage-${i}`).value) || 0,
                    gold: parseInt(document.getElementById(`red-gold-${i}`).value) || 0
                };
                
                if (!bluePlayer.player_id || !redPlayer.player_id) {
                    showMessage('match-error', '모든 플레이어를 선택해주세요');
                    return;
                }
                
                matchData.blue_team.push(bluePlayer);
                matchData.red_team.push(redPlayer);
            }
            
            const response = await fetch('/api/matches', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(matchData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showMessage('match-success', '경기가 등록되었습니다!');
                setTimeout(() => showTab('ranking'), 2000);
            } else {
                showMessage('match-error', result.message);
            }
        }
        
        async function loadPlayerSelect() {
            const response = await fetch('/api/players');
            players = await response.json();
            
            const select = document.getElementById('detail-player-select');
            select.innerHTML = '<option value="">플레이어를 선택하세요</option>';
            
            players.forEach(player => {
                select.innerHTML += `<option value="${player.id}">${player.name}</option>`;
            });
        }
        
        async function loadPlayerDetail() {
            const playerId = document.getElementById('detail-player-select').value;
            if (!playerId) return;
            
            const response = await fetch(`/api/players/${playerId}/detail`);
            const data = await response.json();
            
            const player = data.player;
            const matches = data.matches;
            
            const winRate = player.games_played > 0 ? (player.wins / player.games_played * 100).toFixed(1) : 0;
            const kda = player.deaths > 0 ? ((player.kills + player.assists) / player.deaths).toFixed(2) : (player.kills + player.assists).toFixed(2);
            const avgKills = player.games_played > 0 ? (player.kills / player.games_played).toFixed(1) : 0;
            const avgDeaths = player.games_played > 0 ? (player.deaths / player.games_played).toFixed(1) : 0;
            const avgAssists = player.games_played > 0 ? (player.assists / player.games_played).toFixed(1) : 0;
            
            let html = `
                <div class="player-card">
                    <h2>${player.name}</h2>
                    <div class="player-stats">
                        <div class="stat-box">
                            <div class="stat-value">${player.mmr}</div>
                            <div class="stat-label">MMR</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${player.games_played}</div>
                            <div class="stat-label">총 게임</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${winRate}%</div>
                            <div class="stat-label">승률</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${kda}</div>
                            <div class="stat-label">평균 KDA</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${avgKills} / ${avgDeaths} / ${avgAssists}</div>
                            <div class="stat-label">평균 K/D/A</div>
                        </div>
                    </div>
                </div>
                
                <div class="match-history">
                    <h3>최근 경기 (최대 20경기)</h3>
            `;
            
            matches.forEach(match => {
                const won = (match.team === 'blue' && match.winning_team === 'blue') || 
                           (match.team === 'red' && match.winning_team === 'red');
                const kda = match.deaths > 0 ? ((match.kills + match.assists) / match.deaths).toFixed(2) : (match.kills + match.assists).toFixed(2);
                
                html += `
                    <div class="match-item ${won ? 'win' : 'loss'}">
                        <strong>${won ? '승리' : '패배'}</strong> | 
                        ${match.champion} | 
                        ${match.kills}/${match.deaths}/${match.assists} (KDA: ${kda}) | 
                        딜량: ${match.damage.toLocaleString()} | 
                        골드: ${match.gold.toLocaleString()} | 
                        MMR 변동: ${match.mmr_change > 0 ? '+' : ''}${match.mmr_change}
                        <div style="font-size: 12px; color: #666; margin-top: 5px;">
                            ${new Date(match.match_date).toLocaleString('ko-KR')}
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
            
            document.getElementById('player-detail-content').innerHTML = html;
        }
        
        function showMessage(elementId, message) {
            const el = document.getElementById(elementId);
            el.textContent = message;
            el.style.display = 'block';
            setTimeout(() => el.style.display = 'none', 3000);
        }
        
        // 초기 로드
        loadRanking();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/players', methods=['GET', 'POST'])
def players():
    conn = sqlite3.connect('lol_stats.db')
    c = conn.cursor()
    
    if request.method == 'GET':
        c.execute('SELECT * FROM players ORDER BY mmr DESC, wins DESC')
        players = []
        for row in c.fetchall():
            players.append({
                'id': row[0],
                'name': row[1],
                'mmr': row[2],
                'games_played': row[3],
                'wins': row[4],
                'kills': row[5],
                'deaths': row[6],
                'assists': row[7]
            })
        conn.close()
        return jsonify(players)
    
    elif request.method == 'POST':
        data = request.json
        try:
            c.execute('INSERT INTO players (name) VALUES (?)', (data['name'],))
            conn.commit()
            conn.close()
            return jsonify({'success': True})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': '이미 존재하는 플레이어입니다'})

@app.route('/api/players/<int:player_id>/detail')
def player_detail(player_id):
    conn = sqlite3.connect('lol_stats.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM players WHERE id = ?', (player_id,))
    row = c.fetchone()
    player = {
        'id': row[0],
        'name': row[1],
        'mmr': row[2],
        'games_played': row[3],
        'wins': row[4],
        'kills': row[5],
        'deaths': row[6],
        'assists': row[7]
    }
    
    c.execute('''SELECT ms.*, m.winning_team, m.match_date 
                 FROM match_stats ms
                 JOIN matches m ON ms.match_id = m.id
                 WHERE ms.player_i