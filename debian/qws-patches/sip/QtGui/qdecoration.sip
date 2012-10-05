// qdecoration.sip
//
// Copyright (c) 2008 David Boddie <david@boddie.org.uk>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.


class QDecoration
{

%TypeHeaderCode
#include <qdecoration_qws.h>
%End

public:
    QDecoration();
    virtual ~QDecoration();

    enum DecorationRegion {
        None, All,
        TopLeft, Top, TopRight,
        Left, Right,
        BottomLeft, Bottom, BottomRight,
        Borders,
        Menu, Title, Help,
        Minimize, Maximize, Normalize,
        Close, Move, Resize
    };

    enum DecorationState { Normal, Disabled, Hover, Pressed };

    virtual QRegion region(const QWidget *w, const QRect &rect, int decorationRegion = All ) = 0;
    QRegion region(const QWidget *w, int decorationRegion = All );
    virtual int regionAt(const QWidget *w, const QPoint &point);

    virtual void regionClicked(QWidget *widget, int region);
    virtual void regionDoubleClicked(QWidget *widget, int region);
%If (PyQt_Menu)
    virtual void buildSysMenu(QWidget *widget, QMenu *menu);
    void menuTriggered(QWidget *widget, QAction *action);
%End

    static void startMove(QWidget *widget);
    static void startResize(QWidget *widget);

    virtual bool paint(QPainter *p, const QWidget *w, int decorationRegion = All,
                       DecorationState state = Normal) = 0;
};
