--Copyright (C) 2016 Siavoosh Payandeh Azad

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--use IEEE.math_real."ceil";
--use IEEE.math_real."log2";
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE ieee.numeric_std.ALL;

USE work.router_pack.ALL;
ENTITY router_credit_based IS
    GENERIC (
        DATA_WIDTH : INTEGER := 32;
        current_address : INTEGER := 0;
        Rxy_rst : INTEGER := 10;
        Cx_rst : INTEGER := 10;
        NoC_size_x : INTEGER := 4
    );
    PORT (
        reset, clk : IN std_logic;

        RX_N, RX_E, RX_W, RX_S, RX_L : IN std_logic_vector (DATA_WIDTH - 1 DOWNTO 0);

        credit_in_N, credit_in_E, credit_in_W, credit_in_S, credit_in_L : IN std_logic;
        valid_in_N, valid_in_E, valid_in_W, valid_in_S, valid_in_L : IN std_logic;

        valid_out_N, valid_out_E, valid_out_W, valid_out_S, valid_out_L : OUT std_logic;
        credit_out_N, credit_out_E, credit_out_W, credit_out_S, credit_out_L : OUT std_logic;

        TX_N, TX_E, TX_W, TX_S, TX_L : OUT std_logic_vector (DATA_WIDTH - 1 DOWNTO 0)
    );
END router_credit_based;
ARCHITECTURE behavior OF router_credit_based IS

    SIGNAL FIFO_D_out_N, FIFO_D_out_E, FIFO_D_out_W, FIFO_D_out_S, FIFO_D_out_L : std_logic_vector(DATA_WIDTH - 1 DOWNTO 0);
    SIGNAL Grant_NN, Grant_NE, Grant_NW, Grant_NS, Grant_NL : std_logic;
    SIGNAL Grant_EN, Grant_EE, Grant_EW, Grant_ES, Grant_EL : std_logic;
    SIGNAL Grant_WN, Grant_WE, Grant_WW, Grant_WS, Grant_WL : std_logic;
    SIGNAL Grant_SN, Grant_SE, Grant_SW, Grant_SS, Grant_SL : std_logic;
    SIGNAL Grant_LN, Grant_LE, Grant_LW, Grant_LS, Grant_LL : std_logic;

    SIGNAL Req_NN, Req_EN, Req_WN, Req_SN, Req_LN : std_logic;
    SIGNAL Req_NE, Req_EE, Req_WE, Req_SE, Req_LE : std_logic;
    SIGNAL Req_NW, Req_EW, Req_WW, Req_SW, Req_LW : std_logic;
    SIGNAL Req_NS, Req_ES, Req_WS, Req_SS, Req_LS : std_logic;
    SIGNAL Req_NL, Req_EL, Req_WL, Req_SL, Req_LL : std_logic;

    SIGNAL empty_N, empty_E, empty_W, empty_S, empty_L : std_logic;

    SIGNAL Xbar_sel_N, Xbar_sel_E, Xbar_sel_W, Xbar_sel_S, Xbar_sel_L : std_logic_vector(4 DOWNTO 0);
BEGIN
    ------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------
    -- all the FIFOs
    FIFO_N : FIFO_credit_based
    GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        reset => reset, clk => clk, RX => RX_N, valid_in => valid_in_N,
        read_en_N => '0', read_en_E => Grant_EN, read_en_W => Grant_WN, read_en_S => Grant_SN, read_en_L => Grant_LN,
        credit_out => credit_out_N, empty_out => empty_N, Data_out => FIFO_D_out_N);

    FIFO_E : FIFO_credit_based
    GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        reset => reset, clk => clk, RX => RX_E, valid_in => valid_in_E,
        read_en_N => Grant_NE, read_en_E => '0', read_en_W => Grant_WE, read_en_S => Grant_SE, read_en_L => Grant_LE,
        credit_out => credit_out_E, empty_out => empty_E, Data_out => FIFO_D_out_E);

    FIFO_W : FIFO_credit_based
    GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        reset => reset, clk => clk, RX => RX_W, valid_in => valid_in_W,
        read_en_N => Grant_NW, read_en_E => Grant_EW, read_en_W => '0', read_en_S => Grant_SW, read_en_L => Grant_LW,
        credit_out => credit_out_W, empty_out => empty_W, Data_out => FIFO_D_out_W);

    FIFO_S : FIFO_credit_based
    GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        reset => reset, clk => clk, RX => RX_S, valid_in => valid_in_S,
        read_en_N => Grant_NS, read_en_E => Grant_ES, read_en_W => Grant_WS, read_en_S => '0', read_en_L => Grant_LS,
        credit_out => credit_out_S, empty_out => empty_S, Data_out => FIFO_D_out_S);

    FIFO_L : FIFO_credit_based
    GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        reset => reset, clk => clk, RX => RX_L, valid_in => valid_in_L,
        read_en_N => Grant_NL, read_en_E => Grant_EL, read_en_W => Grant_WL, read_en_S => Grant_SL, read_en_L => '0',
        credit_out => credit_out_L, empty_out => empty_L, Data_out => FIFO_D_out_L);
    ------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------

    -- all the LBDRs
    LBDR_N : LBDR GENERIC MAP(Rxy_rst => Rxy_rst, Cx_rst => Cx_rst)
    PORT MAP(
        reset => reset, clk => clk, empty => empty_N,
        flit_type => FIFO_D_out_N(DATA_WIDTH - 1 DOWNTO DATA_WIDTH - 3),
        cur_addr_y => std_logic_vector(to_unsigned(current_address / NoC_size_x, 7)),
        cur_addr_x => std_logic_vector(to_unsigned(current_address MOD NoC_size_x, 7)),
        dst_addr_y => FIFO_D_out_N(14 DOWNTO 8),
        dst_addr_x => FIFO_D_out_N(7 DOWNTO 1),
        grant_N => '0', grant_E => Grant_EN, grant_W => Grant_WN, grant_S => Grant_SN, grant_L => Grant_LN,
        Req_N => Req_NN, Req_E => Req_NE, Req_W => Req_NW, Req_S => Req_NS, Req_L => Req_NL);

    LBDR_E : LBDR GENERIC MAP(Rxy_rst => Rxy_rst, Cx_rst => Cx_rst)
    PORT MAP(
        reset => reset, clk => clk, empty => empty_E,
        flit_type => FIFO_D_out_E(DATA_WIDTH - 1 DOWNTO DATA_WIDTH - 3),
        cur_addr_y => std_logic_vector(to_unsigned(current_address / NoC_size_x, 7)),
        cur_addr_x => std_logic_vector(to_unsigned(current_address MOD NoC_size_x, 7)),
        dst_addr_y => FIFO_D_out_E(14 DOWNTO 8),
        dst_addr_x => FIFO_D_out_E(7 DOWNTO 1),
        grant_N => Grant_NE, grant_E => '0', grant_W => Grant_WE, grant_S => Grant_SE, grant_L => Grant_LE,
        Req_N => Req_EN, Req_E => Req_EE, Req_W => Req_EW, Req_S => Req_ES, Req_L => Req_EL);

    LBDR_W : LBDR GENERIC MAP(Rxy_rst => Rxy_rst, Cx_rst => Cx_rst)
    PORT MAP(
        reset => reset, clk => clk, empty => empty_W,
        flit_type => FIFO_D_out_W(DATA_WIDTH - 1 DOWNTO DATA_WIDTH - 3),
        cur_addr_y => std_logic_vector(to_unsigned(current_address / NoC_size_x, 7)),
        cur_addr_x => std_logic_vector(to_unsigned(current_address MOD NoC_size_x, 7)),
        dst_addr_y => FIFO_D_out_W(14 DOWNTO 8),
        dst_addr_x => FIFO_D_out_W(7 DOWNTO 1),
        grant_N => Grant_NW, grant_E => Grant_EW, grant_W => '0', grant_S => Grant_SW, grant_L => Grant_LW,
        Req_N => Req_WN, Req_E => Req_WE, Req_W => Req_WW, Req_S => Req_WS, Req_L => Req_WL);

    LBDR_S : LBDR GENERIC MAP(Rxy_rst => Rxy_rst, Cx_rst => Cx_rst)
    PORT MAP(
        reset => reset, clk => clk, empty => empty_S,
        flit_type => FIFO_D_out_S(DATA_WIDTH - 1 DOWNTO DATA_WIDTH - 3),
        cur_addr_y => std_logic_vector(to_unsigned(current_address / NoC_size_x, 7)),
        cur_addr_x => std_logic_vector(to_unsigned(current_address MOD NoC_size_x, 7)),
        dst_addr_y => FIFO_D_out_S(14 DOWNTO 8),
        dst_addr_x => FIFO_D_out_S(7 DOWNTO 1),
        grant_N => Grant_NS, grant_E => Grant_ES, grant_W => Grant_WS, grant_S => '0', grant_L => Grant_LS,
        Req_N => Req_SN, Req_E => Req_SE, Req_W => Req_SW, Req_S => Req_SS, Req_L => Req_SL);

    LBDR_L : LBDR GENERIC MAP(Rxy_rst => Rxy_rst, Cx_rst => Cx_rst)
    PORT MAP(
        reset => reset, clk => clk, empty => empty_L,
        flit_type => FIFO_D_out_L(DATA_WIDTH - 1 DOWNTO DATA_WIDTH - 3),
        cur_addr_y => std_logic_vector(to_unsigned(current_address / NoC_size_x, 7)),
        cur_addr_x => std_logic_vector(to_unsigned(current_address MOD NoC_size_x, 7)),
        dst_addr_y => FIFO_D_out_L(14 DOWNTO 8),
        dst_addr_x => FIFO_D_out_L(7 DOWNTO 1),
        grant_N => Grant_NL, grant_E => Grant_EL, grant_W => Grant_WL, grant_S => Grant_SL, grant_L => '0',
        Req_N => Req_LN, Req_E => Req_LE, Req_W => Req_LW, Req_S => Req_LS, Req_L => Req_LL);

    ------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------

    -- switch allocator

    allocator_unit : allocator PORT MAP(
        reset => reset, clk => clk,
        -- flow control
        credit_in_N => credit_in_N, credit_in_E => credit_in_E, credit_in_W => credit_in_W, credit_in_S => credit_in_S, credit_in_L => credit_in_L,

        -- requests from the LBDRS
        req_N_N => '0', req_N_E => Req_NE, req_N_W => Req_NW, req_N_S => Req_NS, req_N_L => Req_NL,
        req_E_N => Req_EN, req_E_E => '0', req_E_W => Req_EW, req_E_S => Req_ES, req_E_L => Req_EL,
        req_W_N => Req_WN, req_W_E => Req_WE, req_W_W => '0', req_W_S => Req_WS, req_W_L => Req_WL,
        req_S_N => Req_SN, req_S_E => Req_SE, req_S_W => Req_SW, req_S_S => '0', req_S_L => Req_SL,
        req_L_N => Req_LN, req_L_E => Req_LE, req_L_W => Req_LW, req_L_S => Req_LS, req_L_L => '0',
        empty_N => empty_N, empty_E => empty_E, empty_w => empty_W, empty_S => empty_S, empty_L => empty_L,
        valid_N => valid_out_N, valid_E => valid_out_E, valid_W => valid_out_W, valid_S => valid_out_S, valid_L => valid_out_L,
        -- grant_X_Y means the grant for X output port towards Y input port
        -- this means for any X in [N, E, W, S, L] then set grant_X_Y is one hot!
        grant_N_N => Grant_NN, grant_N_E => Grant_NE, grant_N_W => Grant_NW, grant_N_S => Grant_NS, grant_N_L => Grant_NL,
        grant_E_N => Grant_EN, grant_E_E => Grant_EE, grant_E_W => Grant_EW, grant_E_S => Grant_ES, grant_E_L => Grant_EL,
        grant_W_N => Grant_WN, grant_W_E => Grant_WE, grant_W_W => Grant_WW, grant_W_S => Grant_WS, grant_W_L => Grant_WL,
        grant_S_N => Grant_SN, grant_S_E => Grant_SE, grant_S_W => Grant_SW, grant_S_S => Grant_SS, grant_S_L => Grant_SL,
        grant_L_N => Grant_LN, grant_L_E => Grant_LE, grant_L_W => Grant_LW, grant_L_S => Grant_LS, grant_L_L => Grant_LL
    );

    ------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------
    -- all the Xbar select_signals

    Xbar_sel_N <= '0' & Grant_NE & Grant_NW & Grant_NS & Grant_NL;
    Xbar_sel_E <= Grant_EN & '0' & Grant_EW & Grant_ES & Grant_EL;
    Xbar_sel_W <= Grant_WN & Grant_WE & '0' & Grant_WS & Grant_WL;
    Xbar_sel_S <= Grant_SN & Grant_SE & Grant_SW & '0' & Grant_SL;
    Xbar_sel_L <= Grant_LN & Grant_LE & Grant_LW & Grant_LS & '0';
    ------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------
    -- all the Xbars
    XBAR_N : XBAR GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        North_in => FIFO_D_out_N, East_in => FIFO_D_out_E, West_in => FIFO_D_out_W, South_in => FIFO_D_out_S, Local_in => FIFO_D_out_L,
        sel => Xbar_sel_N, Data_out => TX_N);
    XBAR_E : XBAR GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        North_in => FIFO_D_out_N, East_in => FIFO_D_out_E, West_in => FIFO_D_out_W, South_in => FIFO_D_out_S, Local_in => FIFO_D_out_L,
        sel => Xbar_sel_E, Data_out => TX_E);
    XBAR_W : XBAR GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        North_in => FIFO_D_out_N, East_in => FIFO_D_out_E, West_in => FIFO_D_out_W, South_in => FIFO_D_out_S, Local_in => FIFO_D_out_L,
        sel => Xbar_sel_W, Data_out => TX_W);
    XBAR_S : XBAR GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        North_in => FIFO_D_out_N, East_in => FIFO_D_out_E, West_in => FIFO_D_out_W, South_in => FIFO_D_out_S, Local_in => FIFO_D_out_L,
        sel => Xbar_sel_S, Data_out => TX_S);
    XBAR_L : XBAR GENERIC MAP(DATA_WIDTH => DATA_WIDTH)
    PORT MAP(
        North_in => FIFO_D_out_N, East_in => FIFO_D_out_E, West_in => FIFO_D_out_W, South_in => FIFO_D_out_S, Local_in => FIFO_D_out_L,
        sel => Xbar_sel_L, Data_out => TX_L);

END;