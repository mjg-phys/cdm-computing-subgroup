To run with LaTeX fonts, please put these at the top of any notebook. It takes on the order of minutes to do so.

```
! apt install cm-super
! sudo apt-get install texlive-latex-recommended 
! sudo apt-get install dvipng texlive-latex-extra texlive-fonts-recommended 
! wget http://mirrors.ctan.org/macros/latex/contrib/type1cm.zip 
! unzip type1cm.zip -d /tmp/type1cm 
! cd /tmp/type1cm/type1cm/ && sudo latex type1cm.ins
! sudo mkdir /usr/share/texmf/tex/latex/type1cm 
! sudo cp /tmp/type1cm/type1cm/type1cm.sty /usr/share/texmf/tex/latex/type1cm 
! sudo texhash 

```

Add these lines to example.inbpy to get the data on Colab
```
!curl -L -o Data.zip https://github.com/mjg-phys/HowToMakeAPlot/raw/main/PlottingChallenge/Data.zip
!unzip Data.zip 
!rm Data.zip

!curl -L -o Models.zip https://github.com/mjg-phys/HowToMakeAPlot/raw/main/PlottingChallenge/Models.zip
!unzip Models.zip 
!rm Models.zip 