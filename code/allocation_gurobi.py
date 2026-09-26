import gurobipy as gp
from gurobipy import GRB

class BikeAllocationSolver:
    def __init__(self, S, S_R, S_T, S_H, R, N, c, f, B, N_max, gamma, q):
        self.data = {
            'S': S, 'S_R': S_R, 'S_T': S_T, 'S_H': S_H,
            'R': R, 'N': N, 'c': c, 'f': f,
            'B': B, 'N_max': N_max, 'gamma': gamma, 'q': q
        }
        self.model = gp.Model("Bike_Allocation_Core")
        self.results = {}
    
    def solve(self):
        """執行模型求解全過程"""
        self._init_variables()
        self._add_constraints()
        self._set_objective()
        self._optimize()
        return self._extract_solution()

    def _init_variables(self):
        """初始化決策變數"""
        d = self.data
        
        # 選址決策 (二進位)
        self.Y = self.model.addVars(d['S'], vtype=GRB.BINARY, name="Y")
        
        # 投放量決策 (整數)
        self.X = self.model.addVars(d['S'], vtype=GRB.INTEGER, lb=0, name="X")
        
        # 服務缺口變數
        self.alpha = self.model.addVars(d['S'], vtype=GRB.CONTINUOUS, lb=0, name="alpha")
        self.beta = self.model.addVars(d['S'], vtype=GRB.CONTINUOUS, lb=0, name="beta")
        
        # 全域缺口目標
        self.Phi_max = self.model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Phi_max")
        self.Phi_sum = self.model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Phi_sum")

    def _add_constraints(self):
        """構建模型約束系統"""
        d = self.data
        
        # 約束1: 容量約束 (0 ≤ Xₛ ≤ cₛYₛ)
        self.model.addConstrs(self.X[s] <= d['c'][s] * self.Y[s] for s in d['S'])
        self.model.addConstrs(self.X[s] >= 0 for s in d['S'])
        
        # 約束2: 總量約束 (∑Xₛ ≤ B)
        self.model.addConstr(gp.quicksum(self.X[s] for s in d['S']) <= d['B'])
        
        # 約束3: 站點數約束 (∑Yₛ ≤ N_max)
        self.model.addConstr(gp.quicksum(self.Y[s] for s in d['S']) <= d['N_max'])
        
        # 約束4: 即時庫存計算
        G = {}
        for s in d['S']:
            G[s] = [self.X[s]]  # τ=0
            for m in range(1, d['q']+1):
                cum_flow = gp.quicksum(d['f'][s][i] for i in range(m))
                G[s].append(self.X[s] + cum_flow)
        
        # 約束5: 借車缺口定義 (α_s)
        for s in d['S']:
            # α_s ≥ -G_m^s (∀m)
            self.model.addConstrs(self.alpha[s] >= -G[s][m] for m in range(1, d['q']+1))
            self.model.addConstr(self.alpha[s] >= 0)
        
        # 約束6: 還車缺口定義 (β_s)
        for s in d['S']:
            # β_s ≥ G_m^s - c_s (∀m)
            self.model.addConstrs(self.beta[s] >= G[s][m] - d['c'][s] for m in range(1, d['q']+1))
            self.model.addConstr(self.beta[s] >= 0)
        
        # 約束7: 全域最大缺口 (Φ_max)
        for s in d['S']:
            self.model.addConstr(self.Phi_max >= self.alpha[s])
            self.model.addConstr(self.Phi_max >= self.beta[s])
        
        # 約束8: 缺口總和 (Φ_sum)
        self.model.addConstr(
            self.Phi_sum == gp.quicksum(
                (self.alpha[s] + self.beta[s]) * self.Y[s] for s in d['S']
            )
        )
        
        # 約束9: 功能區最小站點數
        self.model.addConstr(
            gp.quicksum(self.Y[s] for s in d['S_R']) >= d['gamma']['R']
        )
        self.model.addConstr(
            gp.quicksum(self.Y[s] for s in d['S_T']) >= d['gamma']['T']
        )
        self.model.addConstr(
            gp.quicksum(self.Y[s] for s in d['S_H']) >= d['gamma']['H']
        )
        
        # 約束10: 居民點可達性
        for r in d['R']:
            self.model.addConstr(
                gp.quicksum(self.Y[s] for s in d['N'][r]) >= 1
            )

    def _set_objective(self):
        """設置目標函數 (λ=0.8)"""
        self.model.setObjective(
            0.8 * self.Phi_max + 0.2 * self.Phi_sum,
            GRB.MINIMIZE
        )

    def _optimize(self):
        """執行優化計算"""
        self.model.setParam('OutputFlag', 0)  # 關閉求解日誌
        self.model.optimize()

    def _extract_solution(self):
        """提取優化結果"""
        if self.model.status == GRB.OPTIMAL:
            return {
                'status': 'OPTIMAL',
                'Y': {s: self.Y[s].X for s in self.data['S']},
                'X': {s: self.X[s].X for s in self.data['S']},
                'alpha': {s: self.alpha[s].X for s in self.data['S']},
                'beta': {s: self.beta[s].X for s in self.data['S']},
                'Phi_max': self.Phi_max.X,
                'Phi_sum': self.Phi_sum.X,
                'obj_value': self.model.ObjVal
            }
        else:
            return {'status': self.model.status}
