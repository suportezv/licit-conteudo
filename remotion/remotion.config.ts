import { existsSync, readdirSync } from "node:fs";
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// O container nao tem Chrome proprio. Usa o headless_shell que vem com o
// Playwright: o Chromium normal de la removeu o headless antigo que o
// Remotion pede, e o download do browser proprio do Remotion esta fora da
// allowlist de rede do environment.
// A pasta carrega o numero da build, e tanto o numero quanto o layout interno
// mudam quando a imagem do container e atualizada:
//   chromium_headless_shell-1194/chrome-linux/headless_shell
//   chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
// Fixar o caminho quebra o render na troca de imagem, entao aqui a maior
// versao instalada e achada em tempo de execucao, nos dois layouts.
const RAIZ = "/opt/pw-browsers";
const LAYOUTS = [
  "chrome-headless-shell-linux64/chrome-headless-shell",
  "chrome-linux/headless_shell",
];
const numero = (nome: string) => Number(nome.split("-").pop());
const shell = existsSync(RAIZ)
  ? readdirSync(RAIZ)
      .filter((d) => d.startsWith("chromium_headless_shell-"))
      .sort((a, b) => numero(b) - numero(a))
      .flatMap((d) => LAYOUTS.map((l) => `${RAIZ}/${d}/${l}`))
      .find((p) => existsSync(p))
  : undefined;
// Fora do container (Mac, por exemplo) nao ha headless_shell do Playwright:
// o Remotion usa o browser que ele mesmo baixa.
if (shell) {
  Config.setBrowserExecutable(shell);
}
