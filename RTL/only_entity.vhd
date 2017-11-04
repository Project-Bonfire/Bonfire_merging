--Copyright (C) 2016 Siavoosh Payandeh Azad

library ieee;
use ieee.std_logic_1164.all;
--use IEEE.STD_LOGIC_ARITH.ALL;
--use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity router_credit_based is
	generic (
        DATA_WIDTH: std_logic_vector(7 downto 0) := 32;
        current_address : integer := 0;
        Cx_rst : integer := 10;
        NoC_size: integer := 4
    );
		
    port (
    reset, clk: in std_logic;

    Rxy_reconf: in  std_logic_vector(7 downto 0);
    Reconfig : in std_logic
    );
end router_credit_based;

architecture behavior of router_credit_based is


end;
